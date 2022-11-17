from applications.application import Application
import sys


class Uniq(Application):
    def exec(self, args, out):
        caseSensitive = True
        if len(args) > 2:
            raise ValueError("wrong number of command line arguments")
        elif len(args) == 0 or len(args) == 1:
            if len(args) == 0:
                self.findUniq(caseSensitive)
            else:
                if args[0] == "-i":
                    caseSensitive = False
                    self.findUniq(caseSensitive)
                else:
                    file = args[0]
                    self.openFile(file, caseSensitive, out)
        else:
            if args[0] != "-i":
                raise ValueError("wrong flags")
            else:
                caseSensitive = False
                file = args[1]
                self.openFile(file, caseSensitive, out)

    def findUniq(self, caseSensitive):
        sin = sys.stdin
        sout = sys.stdout
        ls = []
        ls.append(sin.readline())
        while True:
            try:
                if caseSensitive == True:
                    s = sin.readline()
                    if ls[-1] != s:
                        sout.write(ls[-1])
                        ls[-1] = s
                else:
                    s = sin.readline()
                    if ls[-1].lower() != s.lower():
                        sout.write(ls[-1])
                        ls[-1] = s
            except KeyboardInterrupt:
                break

    def openFile(self, file, caseSensitive, out):
        with open(file) as f:
            lines = f.readlines()
            standardLine = lines[0]
            if caseSensitive == True:
                out.append(standardLine)
                for i in range(1, len(lines)):
                    if lines[i] != lines[i - 1]:
                        out.append(lines[i])
            else:
                out.append(standardLine)
                for i in range(1, len(lines)):
                    if lines[i].lower() != lines[i - 1].lower():
                        out.append(lines[i])
