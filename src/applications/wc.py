import os
from applications.application import Application
from exceptions import InvalidPathError, InvalidFlagError


class Wc(Application):
    """ Outputs the number of lines, words and characters in a file

    It is possible to specify a flag to only output the number of
    lines, words or characters

    Options: -l - number of lines
             -w - number of words
             -m - number of characters
    """

    def exec(self, args, in_stream, out_stream):
        flag = ""
        if len(args) > 0 and args[0][0] == "-":
            flag = args.pop(0)

        # [num_of_lines, num_of_words, num_of_characters]
        total = [0, 0, 0]
        if not len(args) == 0:
            for arg in args:
                if os.path.exists(arg):
                    with open(arg) as f:
                        contents = f.readlines()
                        lines = self.__get_line_count(contents)
                        total[0] += lines
                        words = self.__get_word_count(contents)
                        total[1] += words
                        characters = self.__get_character_count(contents)
                        total[2] += characters
                else:
                    raise InvalidPathError
        else:
            lines = self.__get_line_count(in_stream)
            total[0] += lines
            words = self.__get_word_count(in_stream)
            total[1] += words
            characters = self.__get_character_count(in_stream)
            total[2] += characters

        if flag == '-l':
            out_stream.append("{: >4}".format(str(total[0])+"\n"))
        elif flag == '-w':
            out_stream.append("{: >4}".format(str(total[1])+"\n"))
        elif flag == "-m":
            out_stream.append("{: >4}".format(str(total[2])+"\n"))
        elif flag == "":
            out_stream.append("{: >4} {: >4} {: >4}".format(
                str(total[0]), str(total[1]), str(total[2]))+"\n")
        else:
            raise InvalidFlagError

    def __get_line_count(self, contents):
        return len(contents)

    def __get_word_count(self, contents):
        w = set(list("".join(contents)))
        return len(w)

    def __get_character_count(self, contents):
        c = "".join(contents)
        return len(c)
