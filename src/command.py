import re
from glob import glob
from applications.application import Application


class Command:
    def __init__(self, cmdline):
        self.raw_commands = []
        for m in re.finditer("([^\"';]+|\"[^\"]*\"|'[^']*')", cmdline):
            if m.group(0):
                self.raw_commands.append(m.group(0))

    def eval(self, out):
        for command in self.raw_commands:
            tokens = []
            for m in re.finditer("[^\\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
                if m.group(1) or m.group(2):
                    quoted = m.group(0)
                    tokens.append(quoted[1:-1])
                else:
                    globbing = glob(m.group(0))
                    if globbing:
                        tokens.extend(globbing)
                    else:
                        tokens.append(m.group(0))
            app = tokens[0]
            args = tokens[1:]

            application = Application.by_name(app)
            application.exec(args, out)
