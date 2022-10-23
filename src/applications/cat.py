from applications.application import Application


class Cat(Application):
    def exec(self, args, out):
        for a in args:
            with open(a) as f:
                out.append(f.read())
