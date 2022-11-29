import os

from applications.application import Application
from collections import deque


class History(Application):
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            FILE_PATH = "/comp0010/history.txt"
            try:
                with open(FILE_PATH, "r") as f:
                    self.saved = deque(f.readlines())
            except FileNotFoundError:
                pass

    def exec(self, args, in_stream, out_stream):
        if len(args) > 1:
            raise ValueError("wrong number of command line arguments")

        elif len(args) == 0:
            length = len(self.saved) - 1
            for i in range(length):
                out_stream.append(str(i+1) + "  " + self.saved[i])

        elif (len(args) == 1) and (args[0] == "-c"):
            self.saved.clear()

        else:
            raise ValueError("invalid option")

    def add(self, cmdline):
        self.saved.append(cmdline)
        if len(self.saved) > 100:
            self.saved.popleft()

    def save(self):
        FILE_PATH = "/comp0010/history.txt"
        with open(FILE_PATH, "w") as f:
            for cmdline in self.saved:
                f.write(cmdline)
