import re

from applications.application import Application
from exceptions import WrongNumberOfArgumentsError


class Grep(Application):
    """ Searches for lines containing a match to the specified pattern

    Usage: grep PATTERN [FILE] - PATTERN is a regular expression
    """

    def exec(self, args, in_stream, out_stream):
        if len(args) == 1:
            pattern = args[0]
            while len(in_stream) != 0:
                s = in_stream.popleft()
                if re.search(pattern, s):
                    out_stream.append(s)
        elif len(args) >= 2:
            pattern = args[0]
            files = args[1:]

            for file in files:
                with open(file) as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.rstrip()
                        if re.match(pattern, line):
                            if len(files) > 1:
                                out_stream.append(f"{file}:{line}\n")
                            else:
                                out_stream.append(line + "\n")
        else:
            raise WrongNumberOfArgumentsError
