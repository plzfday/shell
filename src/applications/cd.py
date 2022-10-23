import os
from applications.application import Application


class Cd(Application):
    def exec(self, args, out):
        if len(args) == 0 or len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        os.chdir(args[0])
