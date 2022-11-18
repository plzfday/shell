from applications.application import Application
import sys


class Cat(Application):
    def exec(self, args, out):
        if len(args) != 0:
            for a in args:
                with open(a) as f:
                    out.append(f.read())
        else:
            try:
                while line:=sys.stdin.readline():
                    sys.stdout.write(line)
            except KeyboardInterrupt or EOFError:
                pass

