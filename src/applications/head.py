from applications.application import Application
from exceptions import WrongNumberOfArgumentsError, InvalidFlagError


class Head(Application):
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
            for i in range(min(len(in_stream), num_lines)):
                out_stream.append(in_stream.popleft())
        else:
            file = args[-1]
            with open(file) as f:
                lines = f.readlines()
                for i in range(min(len(lines), num_lines)):
                    line = lines[i].rstrip()
                    out_stream.append(line + "\n")
