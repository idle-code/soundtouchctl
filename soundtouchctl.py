#!/usr/bin/env python3
import libsoundtouch as st
import argparse
from time import sleep


def power_set(dev, on: bool):
    if on:
        print("Turning on")
        dev.power_on()
    else:
        print("Turning off")
        dev.power_off()


def volume_set(dev, level: int):
    print("Setting volume to: " + str(level))
    dev.set_volume(level)

def volume_transition(dev, from_level: int, to_level: int, duration_minutes: float):
    print("Starting smooth volume transition from {} to {}".format(from_level, to_level))
    step_count = abs(to_level - from_level)
    step = 1 if from_level < to_level else -1
    step_delay_sec = duration_minutes*60 / step_count
    print("Delay: {}sec".format(step_delay_sec))

    for s in range(step_count + 1):
        new_level = from_level + step * s
        volume_set(dev, new_level)
        sleep(step_delay_sec)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='action')
    subparsers.add_parser('on')
    subparsers.add_parser('off')
    volume_set_parser = subparsers.add_parser('volume_set')
    volume_set_parser.add_argument('volume_level', action='store', type=int)
    volume_transition_parser = subparsers.add_parser('volume_transition')
    volume_transition_parser.add_argument('from_level', action='store', type=int)
    volume_transition_parser.add_argument('to_level', action='store', type=int)
    volume_transition_parser.add_argument('duration', action='store', type=float)
    smooth_on_parser = subparsers.add_parser('smooth_on')
    smooth_on_parser.add_argument('to_level', action='store', type=int)
    smooth_on_parser.add_argument('duration', action='store', type=float)

    args = parser.parse_args()

    print("Looking up devices...")
    devices = st.discover_devices()
    print("Found {} devices".format(len(devices)))
    dev = devices[0]
    print("Device name: {} - ".format(dev.config.name))
   
    if args.action == 'on':
        power_set(dev, True)
    elif args.action == 'off':
        power_set(dev, False)
    elif args.action == 'volume_set':
        volume_set(dev, args.volume_level)
    elif args.action == 'volume_transition':
        volume_transition(dev, args.from_level, args.to_level, args.duration)
    elif args.action == 'smooth_on':
        # Speaker always start with volume around ~15,
        # which causes the first volume change instruction to be ignored.
        # Following set to 30 overrides that - speaker startsup with provided volume
        # which is immediately overriden by transition routine.
        volume_set(dev, 30)

        power_set(dev, True)
        volume_transition(dev, 1, args.to_level, args.duration)
    else:
        parser.print_help()

