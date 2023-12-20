from __future__ import annotations
import asyncio
from datetime import datetime
from enum import Enum

import necme.protocol as protocol
from necme.types import PowerMode, InputTerminal, GetParamResponse


class Controller(object):
    """
    Represents a connection to one management endpoint, which could in theory
    provide access to multiple monitors. Use ``open_monitor`` or
    ``probe_open_one_monitor`` to obtain a ``Channel`` for a specific
    monitor.

    The documentation for the management protocol requires waiting 600
    milliseconds between consecutive commands, and so the controller and any
    associated channels will collectively enforce that rate limit. Therefore
    making multiple sequential calls will cause a delay on each subsequent
    call.

    In practice this high-level API is designed primarily for the case of
    managing a single monitor by connecting directly to its management port.
    Management of multiple monitors over a single channel is more complicated
    because it means that a single request can potentially return multiple
    responses, without any indication of how many are expected. If you need
    to support that you will probably need to use the lower-level wire protocol
    helpers from ``necme.protocol`` instead.
    """

    def __init__(self, r: asyncio.StreamReader, w: asyncio.StreamWriter):
        """
        Directly wraps an async stream reader and writer as a ``Controller``.

        In most cases it'd be better to use ``Controller.connect_tcpip``.
        """
        self.r = r
        self.w = w
        self.pausing = None

    @classmethod
    async def connect_tcpip(cls, host: str) -> Controller:
        """
        Connects to a management endpoint at the given hostname or IP address,
        returning a ``Controller`` instance if successful.
        """
        reader, writer = await asyncio.open_connection(host, 7142)
        return cls(reader, writer)

    def open_monitor(self, id: int) -> Channel:
        """
        Opens a management channel to the monitor with the given id.

        If you know there's only one monitor available through this controller
        endpoint then you can use ``probe_open_one_monitor`` instead to
        auto-discover its id.
        """
        return Channel(self, protocol.Endpoint.monitor(id))

    async def probe_open_one_monitor(self) -> Channel:
        """
        Probes the management channel to find the id of a monitor that's
        listening on it, and then returns a management channel for that monitor.

        This helper is only correct to use if you know that the management
        endpoint has only one monitor connected to it. If multiple monitors
        respond to the probe then subsequent requests over the same controller
        will misbehave due to interpreting the additional probe responses as
        malformed responses to the subsequent requests.
        """
        chan = Channel(self, protocol.Endpoint.ALL_MONITORS)
        resp = await chan.get_param(0x02, 0x3E)
        return self.open_monitor(resp.value)

    async def null_request(self, dst: protocol.Endpoint) -> protocol.Response:
        """
        Sends a null request to the given endpoint, and returns its response.

        This is here primarily for callers to use to send periodic "keepalive"
        requests if they want to remain connected despite the controller's
        inactivity timeout. It has no other purpose.
        """
        return await self.request(
            dst, protocol.MessageBody(protocol.MessageType.COMMAND, b"BE")
        )

    async def request(
        self, dst: protocol.Endpoint, body: protocol.MessageBody
    ) -> protocol.Response:
        """
        Low-level request API, sending the given message directly to the
        given endpoint and then returning the response directly.

        For simple situations it'll be easier to use the methods on
        ``Channel``, after obtaining an instance using either ``open_monitor``
        or ``probe_open_one_monitor``.
        """
        if self.pausing != None:
            await self.pausing
            self.pausing = None
        req = protocol.Request(dst, body)
        self.w.write(req.as_wire_bytes())
        await self.w.drain()
        resp_raw = await self.r.readuntil(b"\r")
        self.pausing = asyncio.create_task(asyncio.sleep(0.6))
        return protocol.Response.from_wire_bytes(resp_raw)

    async def close(self) -> None:
        """
        Closes the controller's underlying read and write sockets, rendering
        this object useless.
        """
        if self.pausing != None:
            await self.pausing
            self.pausing = None
        self.w.close()
        await self.w.wait_closed()


class Channel(object):
    """
    Represents a connection to a specific single monitor.

    Can also be used to represent connections to other endpoint types, but
    the implementation assumes that only one monitor will respond to each
    request and so it'd be the caller's responsibility to make sure that
    e.g. a selected group has only one monitor in it, etc.
    """

    controller: Controller
    endpoint: protocol.Endpoint

    def __init__(self, controller, endpoint):
        self.controller = controller
        self.endpoint = endpoint

    async def null_request(self) -> protocol.Response:
        """
        Sends a null request to the monitor, and returns its response.

        This is here primarily for callers to use to send periodic "keepalive"
        requests if they want to remain connected despite the controller's
        inactivity timeout. It has no other purpose.
        """
        return await self.controller.null_request(self.endpoint)

    async def get_param(self, code_page: int, code: int) -> GetParamResponse:
        """
        Read a single parameter from the monitor, specified using a code page
        and a code as documented in the management protocol documentation.
        """
        return GetParamResponse(
            await self.controller.request(
                self.endpoint,
                protocol.MessageBody(
                    protocol.MessageType.GET_PARAM,
                    b"%02x%02x" % (code_page, code),
                ),
            )
        )

    async def read_serial_no(self) -> str:
        """
        Read the serial number of the connected monitor as a string.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"C216",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:4].lower() != b"c316":
            raise ValueError("response is not serial number response")
        return protocol.ascii_from_hex_bytes(raw[4:])

    async def read_model_name(self) -> str:
        """
        Read the model name of the connected monitor as a string.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"C217",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:4].lower() != b"c317":
            raise ValueError("response is not model name response")
        return protocol.ascii_from_hex_bytes(raw[4:])

    async def read_firmware_version(self) -> str:
        """
        Read the current firmware version of the connected monitor as a string.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"CA0200",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:8].lower() != b"cb020000":
            raise ValueError("response is not firmware version response")
        return raw[8:].decode("ascii")

    async def read_power_status(self) -> PowerMode:
        """
        Read the current power status of the connected monitor.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"01D6",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:8].lower() != b"0200d600":
            raise ValueError("response is not power status response")
        raw_status = int(raw[-4:], 16)
        return PowerMode(raw_status)

    async def set_power_on(self) -> PowerMode:
        """
        Command the connected monitor to turn on.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"C203D60001",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:8].lower() != b"00c203d6":
            raise ValueError("response is not power set response")
        raw_status = int(raw[-4:], 16)
        return PowerMode(raw_status)

    async def set_power_off(self) -> PowerMode:
        """
        Command the connected monitor to turn off.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"C203D60004",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:8].lower() != b"00c203d6":
            raise ValueError("response is not power set response")
        raw_status = int(raw[-4:], 16)
        return PowerMode(raw_status)

    async def read_active_input(self) -> InputTerminal:
        """
        Read the currently-selected input terminal from the connected monitor.
        """
        resp = await self.get_param(0x00, 0x60)
        return InputTerminal(resp.value)

    async def read_input_name(self, inp: InputTerminal) -> str:
        """
        Read the configured name for a given input terminal, as a string.

        The monitors allow end-user configuration of a display name for each
        input terminal, and this method returns that information. If the user
        has not configured a custom name, the monitor returns its default name
        for the specified terminal.

        The result is the entire string returned by the monitor, which often
        includes some padding spaces at the end. Callers may wish to trim those
        spaces before using the result.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"CA0403%02x" % inp.raw,
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:8].lower() != b"cb040300":
            raise ValueError("response is not input name response")
        return protocol.ascii_from_hex_bytes(raw[10:])

    async def read_datetime(self) -> datetime:
        """
        Read the current date and time from the connected monitor.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"c211",
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:4].lower() != b"c311":
            raise ValueError("response is not date/time response")
        year = int(raw[4:6], 16) + 2000
        month = int(raw[6:8], 16)
        day = int(raw[8:10], 16)
        hour = int(raw[12:14], 16)
        minute = int(raw[14:16], 16)
        return datetime(year, month, day, hour, minute)

    async def write_datetime(self, new: datetime) -> datetime:
        """
        Set the clock of the connected monitor to match the given date and
        time as closely as possible.

        The monitor only supports setting time at a whole-minute granularity,
        so the seconds and any finer interval of the given timestamp are
        ignored. The result is a modified timestamp reflecting what the
        monitor returned as its new understanding of the current date and time.
        """
        resp = await self.controller.request(
            self.endpoint,
            protocol.MessageBody(
                protocol.MessageType.COMMAND,
                b"c212%02x%02x%02x%02x%02x%02x00"
                % (
                    new.year - 2000,
                    new.month,
                    new.day,
                    new.isoweekday() - 1,
                    new.hour,
                    new.minute,
                ),
            ),
        )
        if resp.hdr.typ != protocol.MessageType.COMMAND_REPLY:
            raise ValueError("response is not command reply")
        raw = resp.body.content()
        if raw[0:6].lower() != b"c31200":
            raise ValueError("response is not date/time response")
        year = int(raw[6:8], 16) + 2000
        month = int(raw[8:10], 16)
        day = int(raw[10:12], 16)
        hour = int(raw[14:16], 16)
        minute = int(raw[16:18], 16)
        return datetime(year, month, day, hour, minute)


__all__ = [
    "Controller",
    "Channel",
    "PowerMode",
    "InputTerminal",
]
