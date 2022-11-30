import os

from applications.application import Application
from exceptions import WrongNumberOfArgumentsError


class Cd(Application):
    """ Changes the current working directory """

    def exec(self, args, in_stream, out_stream):
        if len(args) == 0 or len(args) > 1:
            raise WrongNumberOfArgumentsError
        os.chdir(args[0])
