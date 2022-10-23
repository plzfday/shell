from applications.application import Application
from utils import stdinput


class Head(Application):
    def exec(self, args, out):
        if len(args) == 2:
            stdinput()
        else:
            if len(args) != 1 and len(args) != 3:
                raise ValueError("wrong number of command line arguments")
            if len(args) == 1:
                num_lines = 10
                file = args[0]
            if len(args) == 3:
                if args[0] != "-n":
                    raise ValueError("wrong flags")
                else:
                    num_lines = int(args[1])
                    file = args[2]
            with open(file) as f:
                lines = f.readlines()
                for i in range(0, min(len(lines), num_lines)):
                    out.append(lines[i])
