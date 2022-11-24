import abc

from apps import Application
from glob import glob


class Command(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def eval(self, in_stream, out_stream):
        raise NotImplementedError


class Call(Command):
    def __init__(self, app, args):
        self.app = Application.by_name(app)
        self.args = args

    def eval(self, in_stream, out_stream):
        tokens = []
        for each in self.args:
            globbing = glob(each)
            if globbing:
                tokens.extend(globbing)
            else:
                tokens.append(globbing)
        self.app.exec(tokens, in_stream, out_stream)


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
