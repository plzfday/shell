from applications.application import Application
from os import listdir, getcwd


class Ls(Application):
    def exec(self, args, out):
        if len(args) == 0:
            ls_dir = getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = args[0]
        for f in listdir(ls_dir):
            if not f.startswith("."):
                out.append(f + "\n")
