import re, abc, apps

from unsafe_app import UnsafeDecorator


from glob import glob


class Command(metaclass=abc.ABCMeta):
    def __init__(self, cmdline):
        self.raw_commands = []
        for m in re.finditer("([^\"';]+|\"[^\"]*\"|'[^']*')", cmdline):
            if m.group(0):
                self.raw_commands.append(m.group(0))

    def eval(self, in_stream, out_stream):
        for command in self.raw_commands:
            tokens = []

            unsafe_app = False

            if command[0] == "_":
                unsafe_app = True
                command = command[1:]

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

            application = apps.Application.by_name(app)

            if unsafe_app:
                application = UnsafeDecorator(application)

            application.exec(args, in_stream, out_stream)
