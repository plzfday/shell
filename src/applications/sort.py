from applications.application import Application
from exceptions import WrongNumberOfArgumentsError


class Sort(Application):
    """ Sorts the contents of a file/stdin line by line

    Options: -r - sort lines in reverse order
    """

    def exec(self, args, in_stream, out_stream):
        if len(args) > 2:
            raise WrongNumberOfArgumentsError

        contents = []
        is_reverse = False

        if "-r" in args:
            is_reverse = True
            args.remove("-r")

        if len(args) == 0:
            contents = list(in_stream)
        else:
            with open(args[-1], "r") as f:
                for line in f:
                    contents.append(line)

        contents.sort(reverse=is_reverse)

        for line in contents:
            out_stream.append(line)
