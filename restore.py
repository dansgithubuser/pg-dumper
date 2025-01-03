#!/usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('db_name')
parser.add_argument('dump_path')
parser.add_argument('--docker-container')
args = parser.parse_args()

def invoke(invocation, **kwargs):
    kwargs.setdefault('check', True)
    return subprocess.run(invocation.split(), **kwargs)

invocation = f'psql -d {args.db_name}'

if args.docker_container:
    invocation = f'docker exec -i -u postgres {args.docker_container} {invocation}'

with open(args.dump_path) as f:
    invoke(invocation, stdin=f)
