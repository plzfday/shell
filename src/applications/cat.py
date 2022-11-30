from applications.application import Application


class Cat(Application):
    """ Concatenates the content """

    def exec(self, args, in_stream, out_stream):
        if len(args) != 0:
            for arg in args:
                with open(arg) as f:
                    lines = f.readlines()
                    for line in lines:
                        out_stream.append(line.rstrip() + "\n")
        else:
            for line in in_stream:
                out_stream.append(line)
