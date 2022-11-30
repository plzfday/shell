from applications.application import Application


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
            for each in in_stream:
                contents.append(each.rstrip("\n"))
        else:
            with open(args[-1], "r") as f:
                for line in f:
                    contents.append(line.rstrip())

        uniq_contents = self.__process_uniq(contents, case_sensitive)

        for line in uniq_contents:
            out_stream.append(line + "\n")

    def __process_uniq(self, contents, case_sensitive):

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
