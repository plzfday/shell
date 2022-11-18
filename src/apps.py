import sys, re, os, abc


class Application(metaclass=abc.ABCMeta):
    @staticmethod
    def by_name(name):
        app = {
            "pwd": Pwd,
            "cd": Cd,
            "ls": Ls,
            "cat": Cat,
            "echo": Echo,
            "head": Head,
            "tail": Tail,
            "grep": Grep,
            # "cut": Cut,
            "find": Find,
            "uniq": Uniq,
            "sort": Sort,
        }

        if name not in app:
            raise ValueError(f"Unknown application: {name}")

        return app[name]()

    @abc.abstractmethod
    def exec(self, args, in_stream, out_stream):
        raise NotImplementedError


class Pwd(Application):
    def exec(self, args, in_stream, out_stream):
        out_stream.append(os.getcwd() + "\n")


class Cd(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) == 0 or len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        os.chdir(args[0])


class Ls(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = args[0]

        for f in os.listdir(ls_dir):
            if not f.startswith("."):
                out_stream.append(f + "\n")


class Cat(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) != 0:
            for a in args:
                with open(a) as f:
                    out_stream.append(f.read())
        else:
            for line in in_stream:
                out_stream.append(line)


class Echo(Application):
    def exec(self, args, in_stream, out_stream):
        out_stream.append(" ".join(args) + "\n")


class Head(Application):
    def exec(self, args, in_stream, out_stream):
        args_num = len(args)
        if not 1 <= args_num <= 3:
            raise ValueError("wrong number of command line arguments")

        if args_num == 1:
            num_lines = 10
            file = args[0]
        else:
            if args[0] != "-n":
                raise ValueError("wrong flags")

            num_lines = int(args[1])
            if args_num == 3:
                file = args[2]

        if args_num == 2:
            for i in range(min(len(in_stream), num_lines)):
                out_stream.append(in_stream.popleft())
        else:
            with open(file) as f:
                lines = f.readlines()
                for i in range(min(len(lines), num_lines)):
                    out_stream.append(lines[i])


class Tail(Application):
    def exec(self, args, in_stream, out_stream):
        args_num = len(args)
        if not 1 <= args_num <= 3:
            raise ValueError("wrong number of command line arguments")

        if args_num == 1:
            num_lines = 10
            file = args[0]
        else:
            if args[0] != "-n":
                raise ValueError("wrong flags")

            num_lines = int(args[1])
            if args_num == 3:
                file = args[2]

        if args_num == 2:
            display_length = min(len(in_stream), num_lines)
            for i in range(len(in_stream) - display_length):
                in_stream.popleft()
            for i in range(display_length):
                out_stream.append(in_stream.popright())
        else:
            with open(file) as f:
                lines = f.readlines()
                display_length = min(len(lines), num_lines)
                for i in range(display_length):
                    out_stream.append(lines[len(lines) - display_length + i])


class Grep(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) == 1:
            pattern = args[0]
            sin = sys.stdin
            sout = sys.stdout
            while True:
                try:
                    s = sin.readline()
                    if pattern in s:
                        sout.write(s)
                    else:
                        sout.write(s)
                except KeyboardInterrupt:
                    break
        elif len(args) < 2:
            raise ValueError("wrong number of command line arguments")
        elif len(args) == 2:
            pattern = args[0]
            files = args[1:]
            for file in files:
                with open(file) as f:
                    lines = f.readlines()
                    for line in lines:
                        if re.match(pattern, line):
                            if len(files) > 1:
                                out_stream.append(f"{file}:{line}")
                            else:
                                out_stream.append(line)


class Find(Application):
    def exec(self, args, in_stream, out_stream):
        # No argument or more than three arguments
        if len(args) == 0 or len(args) > 3:
            raise ValueError("wrong number of command line arguments")

        # find [PATH] -name PATTERN
        elif len(args) == 3:
            if args[1] != "-name":
                raise ValueError("wrong flags")
            else:
                find_dir = args[0]
                pattern = self.getRegex(args[2])
                for file in self.find(find_dir, pattern):
                    out_stream.append(file + "\n")

        # find -name PATTERN or find . -name(with out pattern)
        elif len(args) == 2:
            if args[1] == "-name":
                raise ValueError("requires pattern")
            if args[0] != "-name":
                raise ValueError("wrong flags")
            else:
                pattern = self.getRegex(args[1])
                for file in self.find(".", pattern):
                    out_stream.append(file + "\n")

        # find [PATH] or find -name(with out pattern)
        elif len(args) == 1:
            if args[0] == "-name":
                raise ValueError("requires pattern")
            find_dir = args[0]
            for file in self.find(find_dir):
                out_stream.append(file + "\n")

    def find(self, dir, pattern=""):
        if dir == "":
            return []
        files = []
        for file in os.scandir(dir):
            if os.path.isdir(file):
                files = files + self.find(dir + "/" + file.name, pattern)
            else:
                if re.match(pattern, file.name):
                    files.append(dir + "/" + file.name)
        return files

    def getRegex(self, pattern):
        regex = pattern.replace(".", "[.]")
        regex = regex.replace("*", ".*")
        if regex[0] == "*":
            regex = regex + "$"

        if regex[:-1] != "*":
            regex = regex + "$"
        return regex


class Uniq(Application):
    def exec(self, args, in_stream, out_stream):
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
                    self.openFile(file, caseSensitive, out_stream)
        else:
            if args[0] != "-i":
                raise ValueError("wrong flags")
            else:
                caseSensitive = False
                file = args[1]
                self.openFile(file, caseSensitive, out_stream)

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


class Sort(Application):
    def exec(self, args, in_stream, out_stream):
        args_num = len(args)
        if args_num > 2:
            raise ValueError("sort: wrong number of arguments")

        contents = []
        is_reverse = False

        if "-r" in args:
            is_reverse = True

        if args_num == 0 or (args_num == 1 and is_reverse):
            contents = list(in_stream)
        else:
            contents = self.__read_file(args[-1])

        contents.sort(reverse=is_reverse)

        for line in contents:
            out_stream.append(line)

    def __read_file(self, path):
        contents = []

        with open(path, "r") as f:
            for line in f:
                contents.append(line.rstrip())

        return contents
