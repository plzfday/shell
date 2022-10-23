from applications.application import Application
import re, sys
from utils import stdinput


class Grep(Application):
    def exec(self, args, out):
        if len(args) == 1:
            pattern = args[0]
            sin = sys.stdin
            sout = sys.stdout
            while True:
                try:
                    s = sin.readline()
                    if pattern in s:
                        sout.write(s)
                    else:
                        sout.write(s)
                except KeyboardInterrupt:
                    break
        elif len(args) < 2:
            raise ValueError("wrong number of command line arguments")
        elif len(args) == 2:
            pattern = args[0]
            files = args[1:]
            for file in files:
                with open(file) as f:
                    lines = f.readlines()
                    for line in lines:
                        if re.match(pattern, line):
                            if len(files) > 1:
                                out.append(f"{file}:{line}")
                            else:
                                out.append(line)
