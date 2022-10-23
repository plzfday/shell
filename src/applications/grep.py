from applications.application import Application
import re


class Grep(Application):
    def exec(self, args, out):
        if len(args) != 2:
            raise ValueError("wrong number of command line arguments")
        pattern = args[0]
        file = args[1]
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if re.search(pattern, line):
                    out.append(line)
