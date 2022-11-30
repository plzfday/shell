from applications.application import Application


class Cat(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) != 0:
            for arg in args:
                with open(arg) as f:
                    out_stream.extend(f.readlines())
        else:
            for line in in_stream:
                out_stream.append(line)
