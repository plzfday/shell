from applications.application import Application
import re, sys


class Grep(Application):
    def exec(self, args, out):
        if len(args) == 1:
            pattern = args[0]
            try:
                while line:=sys.stdin.readline():
                    if re.match(pattern, line):
                        sys.stdout.write(line)
            except KeyboardInterrupt or EOFError:
                pass
        elif len(args) < 2:
            raise ValueError("wrong number of command line arguments")
        elif len(args) >= 2:
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
