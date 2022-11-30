from applications.application import Application
from collections import deque


class History(Application):
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(History, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True
            self.FILE_PATH = "/comp0010/history.txt"
            try:
                with open(self.FILE_PATH, "r") as f:
                    self.saved = deque(f.readlines())
            except FileNotFoundError:
                self.saved = deque()

    def exec(self, args, in_stream, out_stream):
        if len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        elif len(args) == 0:
            for i, item in enumerate(self.saved):
                out_stream.append(f"{i + 1}  {item}")
        elif len(args) == 1 and args[0] == "-c":
            self.saved.clear()
        else:
            raise ValueError("invalid option")

    def add(self, cmdline):
        self.saved.append(cmdline)
        if len(self.saved) > 100:
            self.saved.popleft()

    def save(self):
        with open(self.FILE_PATH, "w") as f:
            for cmdline in self.saved:
                f.write(cmdline + "\n")
