from applications.application import Application


class Echo(Application):
    def exec(self, args, in_stream, out_stream):
        out_stream.append(" ".join(args) + "\n")
