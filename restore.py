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
    if args.docker_container:
        invocation = f'docker exec -i -u postgres {args.docker_container} {invocation}'
    return subprocess.run(invocation.split(), **kwargs)

tables = [
    i
    for i in invoke(f"psql -d {args.db_name} -c \d -t", capture_output=True).stdout.decode().splitlines()
    if i
]
if tables:
    print(
        'Database already has a schema. '
        'This means data must be inserted carefully to avoid constraint errors, which pg_dump does not do. '
        'Enter to proceed, ctrl-c to abort.'
    )
    input()

with open(args.dump_path) as f:
    invoke(f'psql -d {args.db_name}', stdin=f)
