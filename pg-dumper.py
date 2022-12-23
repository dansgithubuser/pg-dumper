#!/usr/bin/env python3

import datetime
import glob
import json
import os
import subprocess

DIR = os.path.dirname(os.path.realpath(__file__))

os.chdir(DIR)

def invoke(invocation, **kwargs):
    kwargs.setdefault('check', True)
    return subprocess.run(invocation.split(), **kwargs)

with open('config.json') as f:
    config = json.load(f)
timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
for db_name, db_config in config.items():
    # create
    dump_name = f'{db_name}_{timestamp}.dump'
    with open(dump_name, 'wb') as f:
        invoke(db_config['cmd'], stdout=f).stdout
    invoke(f'sync {dump_name}')
    print(f'created {dump_name}')
    # remove
    rotate = db_config.get('rotate', 2)
    for dump_name in sorted(glob.glob(f'{db_name}_*.dump'))[:-rotate]:
        os.remove(dump_name)
        print(f'removed {dump_name}')
