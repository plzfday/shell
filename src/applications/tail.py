from applications.application import Application
from exceptions import WrongNumberOfArgumentsError, InvalidFlagError


class Tail(Application):
    """ Prints the last N lines

    Options: -n num - number of lines to print (default 10)
    """

    def exec(self, args, in_stream, out_stream):
        args_num = len(args)
        if args_num > 3:
            raise WrongNumberOfArgumentsError

        num_lines = 10

        if args_num >= 2:
            if args[0] == "-n" and args[1].isdigit():
                num_lines = int(args[1])
            else:
                raise InvalidFlagError

            args_num -= 2

        if args_num == 0:
            display_length = min(len(in_stream), num_lines)
            for i in range(len(in_stream) - display_length):
                in_stream.popleft()
            for i in range(display_length):
                out_stream.append(in_stream.popleft())
        else:
            file = args[-1]
            with open(file) as f:
                lines = f.readlines()
                display_length = min(len(lines), num_lines)
                for i in range(display_length):
                    line = lines[len(lines) - display_length + i].rstrip()
                    out_stream.append(line + "\n")
