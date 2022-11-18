import sys
import os

from collections import deque
from command import Command


def eval(cmdline, in_stream, out_stream):
    command = Command(cmdline)
    command.eval(in_stream, out_stream)


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out_stream = deque()
        eval(sys.argv[2], out_stream)
        while len(out_stream) > 0:
            print(out_stream.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            in_stream = deque()
            out_stream = deque()
            eval(cmdline, in_stream, out_stream)
            while len(out_stream) > 0:
                print(out_stream.popleft(), end="")
