import abc


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
    def __init__(self):
        pass

    def eval(self, in_stream, out_stream):
        pass


class Pipe(Command):
    def __init__(self):
        pass

    def eval(self, in_stream, out_stream):
        pass
