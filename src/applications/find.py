import os
import re
from applications.application import Application


class Find(Application):
    def exec(self, args, in_stream, out_stream):
        # find [PATH] -name PATTERN
        if len(args) == 3:
            if args[1] != "-name":
                raise ValueError("wrong flags")
            else:
                find_dir = args[0]
                pattern = self.__get_regex(args[2])
                for file in self.__find(find_dir, pattern):
                    out_stream.append(file + "\n")

        # find -name PATTERN or find . -name(with out pattern)
        elif len(args) == 2:
            if args[1] == "-name":
                raise ValueError("requires pattern")
            if args[0] != "-name":
                raise ValueError("wrong flags")
            else:
                pattern = self.__get_regex(args[1])
                for file in self.__find(".", pattern):
                    out_stream.append(file + "\n")

        # find [PATH] or find -name(with out pattern)
        elif len(args) == 1:
            if args[0] == "-name":
                raise ValueError("requires pattern")
            find_dir = args[0]
            for file in self.__find(find_dir):
                out_stream.append(file + "\n")

        # No argument or more than three arguments
        else:
            raise ValueError("wrong number of command line arguments")

    def __find(self, dir, pattern=""):
        if dir == "":
            return []
        files = []
        for file in sorted(os.listdir(dir)):
            new_file = os.path.join(dir, file)
            if re.match(pattern, file):
                files.append(new_file)
            if os.path.isdir(new_file) and not os.path.islink(new_file):
                files = files + self.__find(new_file, pattern)
        return files

    def __get_regex(self, pattern):
        regex = pattern
        if regex[0] == "*":
            regex = regex + "$"
        if regex[-1:] != "*":
            regex = regex + "$"
        regex = regex.replace(".", "[.]")
        regex = regex.replace("*", ".*")
        return regex
