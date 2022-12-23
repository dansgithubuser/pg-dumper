#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('user')
parser.add_argument('--hour', default='0')
parser.add_argument('--minute', default='0')
parser.add_argument('--day-of-month', default='*')
parser.add_argument('--month', default='*')
parser.add_argument('--day-of-week', default='0')
args = parser.parse_args()

DIR = os.path.dirname(os.path.realpath(__file__))

with open('/etc/crontab', 'a') as crontab:
    crontab.write(f'{args.minute} {args.hour} {args.day_of_month} {args.month} {args.day_of_week} {args.user} systemd-cat python3 -u {DIR}/pg-dumper.py\n')
