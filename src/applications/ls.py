import os

from applications.application import Application


class Ls(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = args[0]

        for f in sorted(os.listdir(ls_dir)):
            if not f.startswith("."):
                out_stream.append(f + "\n")
