import sys
import os

from collections import deque
from manager import ShellManager


def exec(cmdline, in_stream, out_stream):
    manager = ShellManager(in_stream, out_stream)
    manager.parse(cmdline)


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        in_stream = deque()
        out_stream = deque()
        exec(sys.argv[2], in_stream, out_stream)
        while len(out_stream) > 0:
            print(out_stream.popleft(), end="")
    else:
        FILE_PATH = "/comp0010/history.txt"
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            with open(FILE_PATH, 'a') as f:
                f.write(cmdline + "\n")
            in_stream = deque()
            out_stream = deque()
            exec(cmdline, in_stream, out_stream)
            while len(out_stream) > 0:
                print(out_stream.popleft(), end="")
