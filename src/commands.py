import abc
from collections import deque


class Command(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def eval(self, in_stream, out_stream):
        raise NotImplementedError


class Call(Command):
    def __init__(self):
        pass

    def eval(self, in_stream, out_stream):
        pass


class Sequence(Command):
    def __init__(self, app1: Command, app2: Command):
        self.app1 = app1
        self.app2 = app2

    def eval(self, in_stream, out_stream):
        self.app1.eval(in_stream, out_stream)
        self.app2.eval(in_stream, out_stream)


class Pipe(Command):
    def __init__(self, app1: Command, app2: Call):
        self.app1 = app1
        self.app2 = app2

    def eval(self, in_stream, out_stream):
        self.app1.eval(in_stream, out_stream)
        in_stream = out_stream.copy()
        out_stream.clear()
        self.app2.eval(in_stream, out_stream)
