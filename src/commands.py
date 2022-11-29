import abc

from apps import Application


class Command(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def eval(self, in_stream, out_stream):
        raise NotImplementedError


class Call(Command):
    def __init__(self, app, args, path=""):
        from unsafe_app import UnsafeDecorator
        unsafe_app = False
        if app[0] == "_":
            unsafe_app = True
            app = app[1:]

        self.app = Application.by_name(app)
        if unsafe_app:
            self.app = UnsafeDecorator(self.app)

        self.args = args
        self.path = path

    def eval(self, in_stream, out_stream):
        self.app.exec(self.args, in_stream, out_stream)
        if not self.path == "":
            with open(self.path, "w") as f:
                while not len(out_stream) == 0:
                    f.write(out_stream.popleft())


class Sequence(Command):
    def __init__(self, app1: Command, app2: Command):
        self.app1 = app1
        self.app2 = app2

    def eval(self, in_stream, out_stream):
        # Each <Command> seprated into two branches
        # so each <Command> need a copy of the same out_stream
        # then merged two out_streams together
        out_stream1 = out_stream.copy()
        out_stream2 = out_stream.copy()
        self.app1.eval(in_stream, out_stream1)
        self.app2.eval(in_stream, out_stream2)
        out_stream.extend(out_stream1 + out_stream2)


class Pipe(Command):
    def __init__(self, app1: Command, app2: Call):
        self.app1 = app1
        self.app2 = app2

    def eval(self, in_stream, out_stream):
        self.app1.eval(in_stream, out_stream)
        in_stream = out_stream.copy()
        out_stream.clear()
        self.app2.eval(in_stream, out_stream)
