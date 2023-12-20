"""
Lower-level protocol details for the NE M/ME management protocol.

This module has building blocks for implementing the wire protocol used by the
display management interface, in case the higher-level wrappers in the main
module are insufficient for a particular situation.
"""

from __future__ import annotations
from enum import Enum


class Endpoint(object):
    @classmethod
    def controller(cls) -> Endpoint:
        return cls(b"0")

    @classmethod
    def all_monitors(cls) -> Endpoint:
        return cls(b"*")

    @classmethod
    def monitor(cls, id: int) -> Endpoint:
        if id < 1 or id > 100:
            raise ValueError("id must be between 1 and 100 inclusive")
        raw_val = 0x40 + id
        return cls(bytes([raw_val]))

    @classmethod
    def group(cls, id: int) -> Endpoint:
        if id < 1 or id > 10:
            raise ValueError("id must be between 1 and 10 inclusive")
        raw_val = 0x30 + id
        return cls(bytes([raw_val]))

    def __init__(self, raw: bytes) -> None:
        if len(raw) != 1:
            raise ValueError("raw representation must be exactly one byte")
        self.raw = raw

    def __repr__(self) -> str:
        raw = self.raw[0]
        name = type(self).__name__
        if raw == 0x2A:
            return "%s.ALL_MONITORS" % name
        if raw == 0x30:
            return "%s.CONTROLLER" % name
        elif raw > 0x40 and raw < 0xA5:
            return "%s.monitor(%d)" % (name, raw - 0x40)
        elif raw > 0x30 and raw < 0x3B:
            letter = chr(raw - 0x30 + 0x40)
            return "%s.GROUP_%s" % (name, letter)
        else:
            return "%s(%r)" % (name, self.raw)

    @classmethod
    def from_wire_byte(cls, raw: bytes) -> Endpoint:
        rv = raw[0]
        if rv == 0x2A or (rv >= 0x30 and rv < 0x3B) or (rv > 0x40 and rv < 0xA5):
            return cls(raw)
        raise ValueError("unsupported endpoint type")

    def as_wire_byte(self) -> bytes:
        return self.raw


Endpoint.CONTROLLER = Endpoint.controller()
Endpoint.ALL_MONITORS = Endpoint.all_monitors()
Endpoint.GROUP_A = Endpoint.group(1)
Endpoint.GROUP_B = Endpoint.group(2)
Endpoint.GROUP_C = Endpoint.group(3)
Endpoint.GROUP_D = Endpoint.group(4)
Endpoint.GROUP_E = Endpoint.group(5)
Endpoint.GROUP_F = Endpoint.group(6)
Endpoint.GROUP_G = Endpoint.group(7)
Endpoint.GROUP_H = Endpoint.group(8)
Endpoint.GROUP_I = Endpoint.group(9)
Endpoint.GROUP_J = Endpoint.group(10)


class MessageType(Enum):
    COMMAND = ord("A")
    COMMAND_REPLY = ord("B")
    GET_PARAM = ord("C")
    GET_PARAM_REPLY = ord("D")
    SET_PARAM = ord("E")
    SET_PARAM_REPLY = ord("F")

    def as_wire_byte(self) -> bytes:
        return bytes([self.value])


class MessageHeader(object):
    def __init__(
        self,
        typ: MessageType,
        length: int,
        dst: Endpoint,
        src: Endpoint = Endpoint.CONTROLLER,
    ):
        if length < 2 or length > 255:
            raise ValueError("message length must be between 2 and 255 inclusive")
        self.typ = typ
        self.len = length
        self.dst = dst
        self.src = src

    @classmethod
    def for_raw_body(
        cls, typ: MessageType, dst: Endpoint, body: bytes
    ) -> MessageHeader:
        if len(body) < 2 or body[0] != 0x02 or body[-1] != 0x03:
            raise ValueError("invalid framing for message body")
        return cls(typ, len(body), dst)

    @classmethod
    def for_body(cls, dst: Endpoint, body: MessageBody) -> MessageHeader:
        return cls.for_raw_body(body.typ, dst, body.raw)

    @classmethod
    def from_wire_bytes(cls, raw: bytes) -> MessageHeader:
        if len(raw) != 7:
            raise ValueError("message header must be exactly seven bytes")
        if raw[0] != 0x01:
            raise ValueError("message header does not begin with SOH")
        typ_raw = raw[4]
        dst_raw = raw[2]
        src_raw = raw[3]
        typ = MessageType(typ_raw)
        dst = Endpoint.from_wire_byte(bytes([dst_raw]))
        src = Endpoint.from_wire_byte(bytes([src_raw]))
        length = int(raw[5:7], 16)
        return cls(typ, length, dst, src)

    def as_wire_bytes(self) -> bytes:
        ret = bytearray()
        ret.extend(b"\x010")  # SOH and reserved byte
        ret.extend(self.dst.as_wire_byte())
        ret.extend(self.src.as_wire_byte())
        ret.extend(self.typ.as_wire_byte())
        ret.extend(b"%02x" % self.len)
        return bytes(ret)

    def __repr__(self) -> str:
        return "%s(%s, %s, dst=%s, src=%s)" % (
            type(self).__name__,
            self.typ,
            self.len,
            self.dst,
            self.src,
        )


class MessageBody(object):
    def __init__(self, typ: MessageType, content: bytes):
        self.typ = typ
        self.raw = bytearray(b"\x02")
        self.raw.extend(content)
        self.raw.append(0x03)

    @classmethod
    def from_wire_bytes(cls, typ: MessageType, raw: bytes) -> MessageBody:
        if raw[0] != 0x02 or raw[-1] != 0x03:
            raise ValueError("message body is not correctly framed by STX and ETX")
        ret = cls.__new__(cls)
        ret.typ = typ
        ret.raw = raw
        return ret

    def as_wire_bytes(self) -> bytes:
        return self.raw

    def content(self) -> bytes:
        return self.raw[1:-1]

    def __repr__(self) -> str:
        return "%s(%r, %r)" % (
            type(self).__name__,
            self.typ,
            self.raw,
        )


class Request(object):
    def __init__(self, dst: Endpoint, body: MessageBody):
        hdr = MessageHeader.for_body(dst, body)
        raw = bytearray(hdr.as_wire_bytes())
        raw.extend(body.as_wire_bytes())
        bcc = block_check_code(raw[1:])
        raw.append(bcc)
        raw.append(0x0D)  # CR delimiter
        self.raw = raw

    def as_wire_bytes(self) -> bytes:
        return self.raw


class Response(object):
    def __init__(self, hdr: MessageHeader, body: MessageBody):
        self.hdr = hdr
        self.body = body

    @classmethod
    def from_wire_bytes(cls, raw: bytes) -> Response:
        if len(raw) < 11:
            raise ValueError("message must have at least 11 bytes")
        if raw[-1] != 0x0D:
            raise ValueError("message must end with CR")
        hdr_raw = raw[0:7]
        hdr = MessageHeader.from_wire_bytes(hdr_raw)
        expect_total_len = hdr.len + 9
        if len(raw) != expect_total_len:
            raise ValueError("message header length field disagrees with actual length")
        bcc_bytes = raw[1:-2]
        got_bcc = block_check_code(bcc_bytes)
        want_bcc = raw[-2]
        if got_bcc != want_bcc:
            raise ValueError("message does not match check code")
        body_bytes = raw[7:-2]
        if body_bytes[0] != 0x02:
            raise ValueError("body does not begin with STX")
        if body_bytes[-1] != 0x03:
            raise ValueError("body does not end with ETX")
        body = MessageBody.from_wire_bytes(hdr.typ, body_bytes)
        return cls(hdr, body)

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.hdr, self.body)


def block_check_code(msg: bytes) -> int:
    v = 0
    for b in msg:
        v = v ^ int(b)
    return v


def ascii_from_hex_bytes(raw: bytes) -> str:
    arr = bytearray()
    while len(raw) != 0:
        arr.append(int(raw[0:2], 16))
        raw = raw[2:]
    return arr.decode("ascii")
