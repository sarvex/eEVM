#!/usr/bin/env python3

import os
import sys

ops_filter = ()

ops = ('/', '*', '<<', '>>', '+', '-', 's/')


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def decode_file(file):
    with open(file, 'rb') as f:
        print(f"Decoding {file}")
        decode_data(f.read())

def decode_data(data):
    arg_size = (len(data) - 1) // 2
    if arg_size not in (16, 32, 64):
        err(f"Incorrect argument size: {arg_size}")
        return

    op_index = int(data[0])
    if op_index >= len(ops):
        return
    op = ops[op_index]

    if ops_filter and op not in ops_filter:
        return

    x = int.from_bytes(data[1:1 + arg_size], byteorder='big')
    y = int.from_bytes(data[1 + arg_size:], byteorder='big')

    print(f"argument size: {arg_size}")
    print(x, op, y)
    print(hex(x), op, hex(y))

    if op in ('/', 's/'):
        print("Test:")
        print("{")
        print(f"    {hex(x)}_u512,")
        print(f"    {hex(y)}_u512,")
        print(f"    {hex(x // y)}_u512,")
        print(f"    {hex(x % y)}_u512,")
        print("},")

    if op == 's/':
        ax = (-x) % 2**512
        ay = (-y) % 2**512
        print("Test:")
        print("{")
        print(f"    {hex(ax)}_u512,")
        print(f"    {hex(ay)}_u512,")
        print(f"    {hex(ax // ay)}_u512,")
        print(f"    {hex(ax % ay)}_u512,")
        print("},")


assert len(sys.argv) > 1

path = sys.argv[1]

if (os.path.isfile(path)):
    decode_file(path)
else:
    for root, _, files in os.walk(path):
        for file in files:
            decode_file(os.path.join(root, file))
