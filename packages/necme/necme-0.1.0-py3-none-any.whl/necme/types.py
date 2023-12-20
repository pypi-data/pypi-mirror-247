from enum import Enum
from necme.protocol import Response, MessageType


class GetParamResponse(object):
    def __init__(self, r: Response):
        if r.hdr.typ != MessageType.GET_PARAM_REPLY:
            raise ValueError("response has incorrect message type")
        raw = r.body.content()
        if len(raw) != 16:
            print(repr(raw))
            raise ValueError("get param value response must have 16 characters in body")
        success = int(raw[0:2], 16)
        if success != 0:
            raise UnsupportedPropertyError()

        self.code_page = int(raw[2:4], 16)
        self.code = int(raw[4:6], 16)
        self.param_type = ParameterType(int(raw[6:8], 16))
        self.max_value = int(raw[8:12], 16)
        self.value = int(raw[12:16], 16)

    def __repr__(self):
        return (
            "%s(code_page=0x%02x, code=0x%02x, param_type=%r, max_value=0x%04x, value=0x%04x)"
            % (
                type(self).__name__,
                self.code_page,
                self.code,
                self.param_type,
                self.max_value,
                self.value,
            )
        )


class ParameterType(Enum):
    PERSISTENT = 0
    MOMENTARY = 1


class UnsupportedPropertyError(Exception):
    pass


class PowerMode(Enum):
    ON = 0x0001
    STANDBY = 0x0002
    RESERVED_0003 = 0x0003
    OFF = 0x0004


class InputTerminal(object):
    def __init__(self, v: int):
        if v < 1 or v > 255:
            raise ValueError("input terminal id out of range")
        self.raw = v

    @property
    def builtin_name(self):
        return {
            0x01: "VGA(RGB)",
            0x03: "DVI",
            0x05: "VIDEO",
            0x09: "Tuner",
            0x0C: "VGA(YPbPr)",
            0x0D: "OPTION",
            0x0F: "DisplayPort1",
            0x10: "DisplayPort2",
            0x11: "HDMI1",
            0x12: "HDMI2",
            0x82: "HDMI3",
            0x87: "MP",
            0x88: "COMPUTE MODULE",
        }.get(self.raw, None)

    def __repr__(self):
        return "%s(0x%02x)" % (
            type(self).__name__,
            self.raw,
        )
