from applications.application import Application


class Echo(Application):
    def exec(self, args, out):
        out.append(" ".join(args) + "\n")
