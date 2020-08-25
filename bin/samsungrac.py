#!/usr/bin/env python3
import asyncio
import argparse

from pysamsungrac.samsungrac import SamsungRac


def get_attr(args):
    if args.name or args.all:
        print("Name: " + rac.name)
    if args.description or args.all:
        print("Description: " + rac.description)
    if args.power or args.all:
        print("Power: " + rac.power)
    if args.current_temperature or args.all:
        print("Current temperature: " + str(rac.current_temperature) + " " + rac.temperature_unit)
    if args.target_temperature or args.all:
        print("Target temperature: " + str(rac.target_temperature) + " " + rac.temperature_unit)
    if args.minimum_temperature or args.all:
        print("Minimum temperature: " + str(rac.min_temp) + " " + rac.temperature_unit)
    if args.maximum_temperature or args.all:
        print("Maximum temperature: " + str(rac.max_temp) + " " + rac.temperature_unit)
    if args.hvac_mode or args.all:
        print("HVAC mode: " + rac.hvac_mode)
    if args.hvac_modes or args.all:
        print("HVAC modes: " + str(rac.hvac_modes))
    if args.fan_speed or args.all:
        print("Fan speed: " + str(rac.fan_speed))
    if args.fan_speeds or args.all:
        print("Fan speed: " + str(rac.fan_speeds))
    if args.swing_mode or args.all:
        print("Swing mode: " + rac.swing_mode)
    if args.swing_modes or args.all:
        print("Swing modes: " + str(rac.swing_modes))
    if args.preset_mode or args.all:
        print("Preset mode: " + rac.preset_mode)
    if args.preset_modes or args.all:
        print("Preset modes: " + str(rac.preset_modes))
    if args.sleep_timer or args.all:
        # TODO: 0 - 5 is multiples of 30 mins, so 1 is 30 mins, 2 is 1h, 3 is 1h 30m, up to 2h 30m
        # 6 is 3 h, up to 24 which is 12h
        print("Sleep timer: " + str(rac.sleep_timer))
    if args.purifier or args.all:
        print("Purifier: " + str(rac.purifier))
    if args.filter_time or args.all:
        print("Filter time: " + str(rac.filter_time))
    if args.filter_alarm_time or args.all:
        print("Filter alarm time: " + str(rac.filter_alarm_time))
    if args.filter_alarm or args.all:
        print("Filter alarm: " + str(rac.filter_alarm))
    if args.beep or args.all:
        print("Beep: " + rac.beep)
    if args.cool_capability or args.all:
        print("Cool Capability: " + str(rac.cool_capability) + "kW")
    if args.warm_capability or args.all:
        print("Warm Capability: " + str(rac.warm_capability) + "kW")
    if args.clean or args.all:
        print("Clean: " + rac.autoclean)
    if args.options or args.all:
        print("Options: " + str(rac.options))


def set_attr(args):
    if args.power:
        loop.run_until_complete(rac.set_power(args.power))
    if args.hvac_mode:
        if args.hvac_mode in rac.hvac_modes:
            loop.run_until_complete(rac.set_hvac_mode(args.hvac_mode))
        else:
            raise ValueError('Mode not supported')
    if args.target_temperature:
        if args.target_temperature in range(rac.min_temp, rac.max_temp + 1):
            loop.run_until_complete(rac.set_target_temperature(args.target_temperature))
        else:
            raise ValueError('Temperature out of range')
    if args.fan_speed:
        if args.fan_speed in rac.fan_speeds:
            loop.run_until_complete(rac.set_fan_speed(args.fan_speed))
        else:
            raise ValueError('Fan speed out of range')
    if args.swing_mode:
        if args.swing_mode in rac.swing_modes:
            loop.run_until_complete(rac.set_swing_mode(args.swing_mode))
        else:
            raise ValueError('Invalid swing mode')
    if args.preset_mode:
        if args.preset_mode in rac.preset_modes:
            loop.run_until_complete(rac.set_preset(args.preset_mode))
        else:
            raise ValueError('Invalid preset')
    if args.sleep_timer:
        if args.sleep_timer in range(1, 24 + 1):
            loop.run_until_complete(rac.set_sleep_timer(args.sleep_timer))
        else:
            raise ValueError('Timer out of range')
    if args.purifier:
        loop.run_until_complete(rac.set_purifier(args.purifier))
    if args.beep:
        loop.run_until_complete(rac.set_beep(args.beep))
    if args.filter_alarm_time:
        loop.run_until_complete(rac.set_filter_alarm_time(args.filter_alarm_time))
    if args.reset_filter:
        print("Sorry, not implemented yet")
    if args.clean:
        loop.run_until_complete(rac.set_clean(args.clean))


parser = argparse.ArgumentParser(description="Samsung RAC wireless interface")
parser.add_argument('--address', required=True)
parser.add_argument('--token', required=True)

# Main commands
subparsers = parser.add_subparsers(help='supported commands')
parser_get = subparsers.add_parser("get")
parser_set = subparsers.add_parser("set")
parser_get_token = subparsers.add_parser("get_token")

# Set commands
parser_set.set_defaults(func=set_attr)
parser_set.add_argument('--power', choices=['On','Off'], help='Set power state')
parser_set.add_argument('--hvac_mode', help='Set HVAC mode')
parser_set.add_argument('--target_temperature', help='Set target temperature', type=int)
parser_set.add_argument('--fan_speed', help='Set fan speed', type=int)
parser_set.add_argument('--swing_mode', help='Set swing mode')
parser_set.add_argument('--preset_mode', help='Set preset mode')
parser_set.add_argument('--sleep_timer', help='Set sleep timer', type=int)
parser_set.add_argument('--purifier', choices=['On','Off'], help='Enable air purifier')
parser_set.add_argument('--beep', choices=['On','Off'], help='Enable/disable beep')
parser_set.add_argument('--filter_alarm_time', help='Set filter alarm time', type=int)
parser_set.add_argument('--reset_filter', action='store_true', help='Reset filter alarm')
parser_set.add_argument('--clean', choices=['On','Off'], help='Set unit autoclean')

# Get commands
parser_get.set_defaults(func=get_attr)
parser_get.add_argument('--all', action='store_true', help='shows all supported attributes')
parser_get.add_argument('--name', action='store_true', help='Name of the AC unit')
parser_get.add_argument('--description', action='store_true', help='Description of the AC unit')
parser_get.add_argument('--power', action='store_true', help='Current power state')
parser_get.add_argument('--current_temperature', action='store_true', help='Current room temperature')
parser_get.add_argument('--target_temperature', action='store_true', help='Current target temperature')
parser_get.add_argument('--maximum_temperature', action='store_true', help='Maximum supported temperature')
parser_get.add_argument('--minimum_temperature', action='store_true', help='Minimum supported temperature')
parser_get.add_argument('--hvac_mode', action='store_true', help='Current HVAC mode')
parser_get.add_argument('--hvac_modes', action='store_true', help='Supported HVAC modes')
parser_get.add_argument('--fan_speed', action='store_true', help='Current fan speed')
parser_get.add_argument('--fan_speeds', action='store_true', help='Supported fan speeds')
parser_get.add_argument('--swing_mode', action='store_true', help='Current swing mode')
parser_get.add_argument('--swing_modes', action='store_true', help='Supported swing modes')
parser_get.add_argument('--preset_mode', action='store_true', help='Current preset mode')
parser_get.add_argument('--preset_modes', action='store_true', help='Supported preset modes')
parser_get.add_argument('--sleep_timer', action='store_true', help='Sleep timer value')
parser_get.add_argument('--cool_capability', action='store_true', help='Cooling capability of the unit')
parser_get.add_argument('--warm_capability', action='store_true', help='Heating capability of the unit')
parser_get.add_argument('--purifier', action='store_true', help='Current state of air purifier')
parser_get.add_argument('--beep', action='store_true', help='State of the beeper')
parser_get.add_argument('--filter_time', action='store_true', help='Amount of time since last filter cleaning')
parser_get.add_argument('--filter_alarm_time', action='store_true', help='Filter alarm time')
parser_get.add_argument('--filter_alarm', action='store_true', help='Filter cleaning alarm')
parser_get.add_argument('--clean', action='store_true', help='Unit self-cleaning')
parser_get.add_argument('--options', action='store_true', help='All unit suboptions')

args = parser.parse_args()
loop = asyncio.get_event_loop()
rac = SamsungRac(args.address, args.token)
loop.run_until_complete(rac.update())
args.func(args)
