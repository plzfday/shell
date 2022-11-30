import os

from applications.application import Application
from exceptions import WrongNumberOfArgumentsError


class Pwd(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) > 0:
            raise WrongNumberOfArgumentsError
        out_stream.append(os.getcwd() + "\n")
