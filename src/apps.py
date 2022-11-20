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
            "cut": Cut,
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
                out_stream.append(in_stream.popleft())
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
            while len(in_stream) != 0:
                s = in_stream.popleft()
                if pattern in s:
                    out_stream.append(s)
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


class Cut(Application):
    def exec(self, args, in_stream, out_stream):
        # cut -b 1 requirements.txt
        # args: ['-b', '1-,3-5', 'requirements.txt']
        if len(args) < 2 or len(args) > 3:
            raise ValueError("Invalid number of arguments")

        if args[0] == "-b":
            intervals = self.__merge_intervals(args[1])
            if len(args) == 2:
                for line in in_stream:
                    self.__print_line(line, intervals, out_stream)
            else:
                with open(args[2], "r") as f:
                    for line in f:
                        self.__print_line(line, intervals, out_stream)
        else:
            raise ValueError("Invalid option")

    def __merge_intervals(self, arg):
        return self.__clean_up_intervals(self.__parse_intervals(arg))

    def __parse_intervals(self, arg):
        intervals = []
        items = arg.split(",")
        for item in items:
            tmp = item.split("-")
            if len(tmp) == 1:
                intervals.append([int(tmp[0]), int(tmp[0])])
            elif len(tmp) == 2:
                if tmp == ("", ""):
                    raise ValueError("Invalid range")
                elif tmp[0] == "":
                    # Case: -num2
                    intervals.append((1, int(tmp[1])))
                elif tmp[1] == "":
                    # Case: num1-
                    # Assume that the max range is up to 1 << 32 - 1
                    intervals.append((int(tmp[0]), 1 << 32 - 1))
                else:
                    # Case: num1-num2
                    n0, n1 = int(tmp[0]), int(tmp[1])
                    if n0 <= n1:
                        intervals.append((n0, n1))
            else:
                raise ValueError("Invalid input")

        return intervals

    def __clean_up_intervals(self, intervals):
        intervals.sort()

        merged = []
        for interval in intervals:
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))

        return merged

    def __print_line(self, line, intervals, out_stream):
        for interval in intervals:
            out_stream.append(line[interval[0] - 1 : interval[1]] + "\n")


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
        if len(args) > 2:
            raise ValueError("wrong number of command line arguments")

        case_sensitive = True
        if "-i" in args and len(args) > 0:
            case_sensitive = False
            args.remove("-i")

        contents = []
        if len(args) == 0:
            contents = list(in_stream)
        else:
            with open(args[-1], "r") as f:
                for line in f:
                    contents.append(line)

        uniq_contents = self.__process_uniq(contents, case_sensitive)

        for line in uniq_contents:
            out_stream.append(line.rstrip())

    def __process_uniq(self, contents, case_sensitive):
        if len(contents) < 2:
            return contents

        result = []
        cmp = 0
        idx = 1

        while idx < len(contents):
            line1 = contents[cmp]
            line2 = contents[idx]

            if not case_sensitive:
                line1 = line1.lower()
                line2 = line2.lower()

            if line1 != line2:
                result.append(contents[cmp])
                cmp = idx

            idx += 1

        result.append(contents[cmp])

        return result


class Sort(Application):
    def exec(self, args, in_stream, out_stream):
        if len(args) > 2:
            raise ValueError("sort: wrong number of arguments")

        contents = []
        is_reverse = False

        if "-r" in args:
            is_reverse = True
            args.remove("-r")

        if len(args) == 0:
            contents = list(in_stream)
        else:
            with open(args[-1], "r") as f:
                for line in f:
                    contents.append(line)

        contents.sort(reverse=is_reverse)

        for line in contents:
            out_stream.append(line)
