import os

from applications.application import Application


class History(Application):
    def exec(self, args, in_stream, out_stream):
        FILE_PATH = "/comp0010/history.txt"
        if len(args) > 1:
            raise ValueError("wrong number of command line arguments")

        elif len(args) == 0:
            with open(FILE_PATH, "r") as f:
                lines = f.readlines()
                for order in range(len(lines)):
                    line = lines[order]
                    out_stream.append(str(order+1) + "  " + line)

        elif (len(args) == 1) and (args[0] == "-c"):
            os.remove(FILE_PATH)

        else:
            raise ValueError("invalid option")
