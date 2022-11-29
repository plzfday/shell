import abc


class Application(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def exec(self, args, in_stream, out_stream):
        raise NotImplementedError
