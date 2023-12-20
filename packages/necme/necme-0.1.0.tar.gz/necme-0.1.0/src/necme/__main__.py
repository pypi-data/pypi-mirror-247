import asyncio
import sys

from necme import Controller, Channel, PowerMode


async def main():
    # If an article ID is given, then show the article
    if len(sys.argv) < 3 or sys.argv[1] == "--help":
        print("Usage: python -m necme <hostname> <command> [arguments...]\n")
        print("Commands:")
        print("  info    Show model name, serial number, and firmware version")
        print("          of the connected monitor.")
        print("  status  Show current power status and selected input.")
        print("  on      Command the monitor to turn on.")
        print("  off     Command the monitor to turn off.")
        return

    hostname = sys.argv[1]
    command = sys.argv[2]

    ctrl = await Controller.connect_tcpip(hostname)
    monitor = await ctrl.probe_open_one_monitor()

    cmd_func = globals().get("cmd_" + command, None)
    if cmd_func is None:
        sys.stdout.write("Unsupported command '%s'\n" % command)
        return 1

    return await cmd_func(monitor, sys.argv[3:])


async def cmd_info(monitor: Channel, args: list) -> int:
    model = await monitor.read_model_name()
    serial = await monitor.read_serial_no()
    firmware = await monitor.read_firmware_version()
    print("Model:         %s" % model)
    print("Serial number: %s" % serial)
    print("Firmware ver.: %s" % firmware)
    return 0


async def cmd_status(monitor: Channel, args: list) -> int:
    power_mode = await monitor.read_power_status()
    print("Power: %s" % power_mode)
    if power_mode != PowerMode.ON:
        return 0

    input = await monitor.read_active_input()
    input_name = (await monitor.read_input_name(input)).strip()
    builtin_name = input.builtin_name
    if input_name != builtin_name:
        print("Input: %s (%s)" % (input_name, builtin_name))
    else:
        print("Input: %s" % input_name)
    return 0


async def cmd_on(monitor: Channel, args: list) -> int:
    await monitor.set_power_on()
    return 0


async def cmd_off(monitor: Channel, args: list) -> int:
    await monitor.set_power_off()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
