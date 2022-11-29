import os

from applications.application import Application


class Pwd(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) > 0:
            raise ValueError("wrong number of command line arguments")
        out_stream.append(os.getcwd() + "\n")
