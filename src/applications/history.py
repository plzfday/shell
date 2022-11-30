from applications.application import Application
from collections import deque
from exceptions import InvalidFlagError, WrongNumberOfArgumentsError


class History(Application):
    """ Prints the preceding commands

    Options: -c - clear the history
    """

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(History, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            cls._init = True
            self.saved = deque()

    def exec(self, args, in_stream, out_stream):
        if len(args) > 1:
            raise WrongNumberOfArgumentsError
        elif len(args) == 0:
            for i, item in enumerate(self.saved):
                out_stream.append(f"{i + 1}  {item}\n")
        elif len(args) == 1 and args[0] == "-c":
            self.saved.clear()
        else:
            raise InvalidFlagError

    def add(self, cmdline):
        self.saved.append(cmdline)
        if len(self.saved) > 100:
            self.saved.popleft()
