import os

from applications.application import Application
from exceptions import WrongNumberOfArguments


class Cd(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) == 0 or len(args) > 1:
            raise WrongNumberOfArguments
        os.chdir(args[0])
