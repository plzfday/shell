from applications.application import Application


class Tail(Application):
    def exec(self, args, in_stream, out_stream):
        args_num = len(args)
        if args_num > 3:
            raise ValueError("wrong number of command line arguments")

        num_lines = 10

        if args_num >= 2:
            if args[0] == "-n":
                try:
                    num_lines = int(args[1])
                except ValueError:
                    raise ValueError("wrong flags")
            else:
                raise ValueError("wrong flags")

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
