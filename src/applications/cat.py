from applications.application import Application
from utils import stdinput


class Cat(Application):
    def exec(self, args, out):
        if len(args) != 0:
            for a in args:
                with open(a) as f:
                    out.append(f.read())
        else:
            stdinput()
