import os
import re

from applications.application import Application
from exceptions import WrongNumberOfArgumentsError, \
    PatternNotFoundError, InvalidFlagError


class Find(Application):
    def exec(self, args, in_stream, out_stream):
        flag = ""
        pattern = ""
        if len(args) == 1 and len(args[0]) > 0 and args[0][0] == "-":
            flag = args.pop()
        elif len(args) == 2 and len(args[-1]) > 0 and args[-1][0] == "-":
            flag = args.pop()
        elif len(args) >= 2 and len(args[-2]) > 0 and args[-2][0] == "-":
            pattern = args.pop()
            flag = args.pop()

        if not flag == "-name" and not flag == "":
            raise InvalidFlagError
        elif flag == "-name" and pattern == "":
            raise PatternNotFoundError

        # find [PATH] -name PATTERN
        if len(args) == 1 and pattern != "":
            find_dir = args[0]
            pattern = self.__get_regex(pattern)
            for file in self.__find(find_dir, pattern):
                out_stream.append(file + "\n")

        # find [PATH]
        elif len(args) == 1 and pattern == "":
            find_dir = args[0]
            for file in self.__find(find_dir):
                out_stream.append(file + "\n")

        # find -name PATTERN
        elif len(args) == 0 and pattern != "":
            pattern = self.__get_regex(pattern)
            for file in self.__find(".", pattern):
                out_stream.append(file + "\n")

        # No argument or more than three arguments
        else:
            raise WrongNumberOfArgumentsError

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
