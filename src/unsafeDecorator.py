import sys, re, os, abc
from apps import Application


class MyError(Exception):
    pass
class MyError2(Exception):
    pass

class UnsafeApplication(Application):
    def __init__(self, application):
        self.application = application
        
    def by_name(self, name):
        self.application.app.update({
            "_pwd": Pwd,
            "_cd": Cd,
            "_ls": Ls,
            "_cat": Cat,
            "_echo": Echo,
            "_head": Head,
            "_tail": Tail,
            "_grep": Grep,
            "_cut": Cut,
            "_find": Find,
            "_uniq": Uniq,
            "_sort": Sort,
        })
        
        try:
            if name not in self.application.app:
                raise MyError
            return self.application.app[name]()
        except:
            print(f"Unknown application: {name}")

class Pwd(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        out_stream.append(os.getcwd() + "\n")


class Cd(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        try:
            if len(args) == 0 or len(args) > 1:
                raise MyError
            os.chdir(args[0])
        except MyError:
            print("wrong number of command line arguments")
    


class Ls(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        try:
            if len(args) == 0:
                ls_dir = os.getcwd()
            elif len(args) > 1:
                raise MyError
            else:
                ls_dir = args[0]
            for f in os.listdir(ls_dir):
                if not f.startswith("."):
                    out_stream.append(f + "\n")
        except MyError:
            print("wrong number of command line arguments")




class Cat(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        if len(args) != 0:
            for a in args:
                with open(a) as f:
                    out_stream.append(f.read())
        else:
            for line in in_stream:
                out_stream.append(line)


class Echo(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        out_stream.append(" ".join(args) + "\n")


class Head(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        try:
            args_num = len(args)
            if not 1 <= args_num <= 3:
                raise MyError

            if args_num == 1:
                num_lines = 10
                file = args[0]
            else:
                if args[0] != "-n":
                    raise MyError2

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
        except MyError:
            print("wrong number of command line arguments")
        except MyError2:
            print("wrong flags")



class Tail(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        try:
            args_num = len(args)
            if not 1 <= args_num <= 3:
                raise MyError

            if args_num == 1:
                num_lines = 10
                file = args[0]
            else:
                if args[0] != "-n":
                    raise MyError2

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
        except MyError:
            print("wrong number of command line arguments")
        except MyError2:
            print("wrong flags")



class Grep(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        try:
            if len(args) == 1:
                pattern = args[0]
                while len(in_stream) != 0:
                    s = in_stream.popleft()
                    if pattern in s:
                        out_stream.append(s)

            elif len(args) >= 2:
                pattern = args[0]
                files = args[1:]
                for file in files:
                    with open(file) as f:
                        lines = f.readlines()
                        for line in lines:
                            line = line.rstrip()
                            if re.match(pattern, line):
                                if len(files) > 1:
                                    out_stream.append(f"{file}:{line}" + "\n")
                                else:
                                    out_stream.append(line+"\n")

            else:
                raise MyError
        except MyError:
            print("wrong number of command line arguments")

class Cut(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        # cut -b 1 requirements.txt
        # args: ['-b', '1-,3-5', 'requirements.txt']
        try:
            if len(args) < 2 or len(args) > 3:
                raise MyError

            if args[0] == "-b":
                intervals = self.__merge_intervals(args[1])
                if len(args) == 2:
                    for line in in_stream:
                        self.__print_line(line.rstrip(), intervals, out_stream)
                else:
                    with open(args[2], "r") as f:
                        for line in f:
                            self.__print_line(line.rstrip(), intervals, out_stream)
            else:
                raise MyError2
        except MyError:
            print("Invalid number of arguments")
        except MyError2:
            print("Invalid option")

    def __merge_intervals(self, arg):
        return self.__clean_up_intervals(self.__parse_intervals(arg))

    def __parse_intervals(self, arg):
        try:
            intervals = []
            items = arg.split(",")
            for item in items:
                tmp = item.split("-")
                if len(tmp) == 1:
                    intervals.append([int(tmp[0]), int(tmp[0])])
                elif len(tmp) == 2:
                    if tmp == ("", ""):
                        raise MyError
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
                    raise MyError2

            return intervals
        except MyError:
            print("Invalid range")
        except MyError2:
            print("Invalid input")


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
        tmp = []
        for interval in intervals:
            tmp.append(line[interval[0] - 1 : interval[1]])
        out_stream.append("".join(tmp) + "\n")


class Find(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        # No argument or more than three arguments
        try:
            if len(args) == 0 or len(args) > 3:
                raise MyError 

            # find [PATH] -name PATTERN
            elif len(args) == 3:
                try:
                    if args[1] != "-name":
                        raise MyError
                    else:
                        find_dir = args[0]
                        pattern = self.getRegex(args[2])
                        for file in self.find(find_dir, pattern):
                            out_stream.append(file + "\n")
                except MyError:
                    print("wrong flags")

            # find -name PATTERN or find . -name(with out pattern)
            elif len(args) == 2:
                try:
                    if args[1] == "-name":
                        raise MyError 
                    if args[0] != "-name":
                        raise MyError2 
                    else:
                        pattern = self.getRegex(args[1])
                        for file in self.find(".", pattern):
                            out_stream.append(file + "\n")
                except MyError:
                    print("requires pattern")
                except MyError2:
                    print("wrong flags")


            # find [PATH] or find -name(with out pattern)
            elif len(args) == 1:
                try:
                    if args[0] == "-name":
                        raise MyError 
                    find_dir = args[0]
                    for file in self.find(find_dir):
                        out_stream.append(file + "\n")
                except MyError:
                    print("requires pattern")

        except MyError:
            print("wrong number of command line arguments")

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


class Uniq(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        caseSensitive = True
        if len(args) > 2:
            print("wrong number of command line arguments")
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
                print("wrong flags")
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


class Sort(UnsafeApplication):
    def exec(self, args, in_stream, out_stream):
        try:
            args_num = len(args)
            if args_num > 2:
                raise MyError
                
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
        except MyError:
            print("sort: wrong number of arguments")

    def __read_file(self, path):
        contents = []

        with open(path, "r") as f:
            for line in f:
                contents.append(line.rstrip())

        return contents
