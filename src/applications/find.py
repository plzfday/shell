import os
import re
from applications.application import Application


class Find(Application):
    def exec(self, args, out):
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
                    out.append(file + "\n")

        # find -name PATTERN
        elif len(args) == 2:
            if args[0] != "-name":
                    raise ValueError("wrong flags")
            else:
                pattern = self.getRegex(args[1])
                for file in self.find('.', pattern):
                    out.append(file + "\n")

        # find [PATH]
        elif len(args) == 1:
            find_dir = args[0]
            for file in self.find(find_dir):
                out.append(file + "\n")

    def find(self, dir, pattern = ""):
        if dir == "":
            return []
        files = []
        for file in os.scandir(dir):
            if os.path.isdir(file):
                files = files + self.find(dir + '/' + file.name, pattern)
            else:
                if re.match(pattern, file.name):
                    files.append(dir + '/'+ file.name)
        return files

    def getRegex(self, pattern):
        regex = pattern.replace('.', '[.]')
        regex = regex.replace('*', '.*')
        if regex[0] == '*':
            regex = regex + '$'
            
        if regex[:-1] != '*':
            regex = regex + '$'
        return regex


