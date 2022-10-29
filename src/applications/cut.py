import sys

from applications.application import Application


class Cut(Application):
    def exec(self, args, out):
        # cut -b 1 requirements.txt
        # args: ['-b', '1-,3-5', 'requirements.txt']
        if len(args) < 2 or len(args) > 3:
            raise ValueError("Invalid number of arguments")

        if args[0] == "-b":
            intervals = self.__merge_intervals(args[1])
            if len(args) == 2:
                try:
                    while line := sys.stdin.readline():
                        self.__print_line(line, intervals, out)
                except KeyboardInterrupt or EOFError:
                    pass
            else:
                with open(args[2], "r") as f:
                    for line in f:
                        self.__print_line(line, intervals, out)
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

    def __print_line(self, line, intervals, out):
        for interval in intervals:
            sys.stdout.write(line.strip()[interval[0] - 1 : interval[1]])
        sys.stdout.write("\n")
