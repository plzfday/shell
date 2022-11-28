import os

import unittest

from unittest.mock import patch

from collections import deque


class TestPwd(unittest.TestCase):
    def setUp(self):
        from src.apps import Pwd

        self.app = Pwd()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_out = ["/comp0010\n"]

    def test_pwd(self):
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_pwd_too_many_arguments(self):
        try:
            self.app.exec(["foo"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")


class TestCd(unittest.TestCase):
    def setUp(self):
        from src.apps import Cd

        self.app = Cd()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_path = "tools"
        self.sample_out = "/comp0010/tools"

    def test_cd(self):
        self.app.exec([self.sample_path], self.in_stream, self.out_stream)
        self.assertEqual(os.getcwd(), self.sample_out)

    def test_cd_no_path(self):
        try:
            self.app.exec([], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")

    def test_cd_too_many_args(self):
        try:
            self.app.exec(["foo", "bar"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")

    def tearDown(self):
        self.app.exec(["/comp0010"], self.in_stream, self.out_stream)


class TestLs(unittest.TestCase):
    def setUp(self):
        from src.apps import Ls

        self.app = Ls()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_path = "tools"
        # results of "ls /comp0010/tools"
        self.sample_out = ["analysis\n", "coverage\n", "test\n"]
        # the number of results of "ls comp0010"
        self.sample_out_number = 12

    def test_ls(self):
        self.app.exec([self.sample_path], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_ls_stdin(self):
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(len(self.out_stream), self.sample_out_number)

    def test_ls_too_many_args(self):
        try:
            self.app.exec(["foo", "bar"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")


class TestCat(unittest.TestCase):
    def setUp(self):
        from src.apps import Cat

        self.app = Cat()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = ["Hi", "My name is", "hello world!"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_out = ["Hi", "My name is", "hello world!"]
        self.sample_out = [x + "\n" for x in self.sample_out]

        with open("test/test_cat.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_cat(self):
        self.app.exec(["test/test_cat.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_cat_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


class TestEcho(unittest.TestCase):
    def setUp(self):
        from src.apps import Echo

        self.app = Echo()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = "Hi my name is"
        self.sample_out = ["Hi my name is\n"]

    def test_echo(self):
        self.app.exec([self.sample_in], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


class TestHead(unittest.TestCase):
    def setUp(self):
        from src.apps import Head

        self.app = Head()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = [" A", "B", "C", "D", "E", "F",
                          "G", "H", "i", "j", " are alphabet"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_less_in = [" A", "B", "C", "D", "E"]
        self.sample_less_in = [x + "\n" for x in self.sample_less_in]

        self.sample_option_out = [" A", "B", "C", "D", "E", "F",
                                  "G", "H", "i", "j", " are alphabet"]
        self.sample_option_out = [x + "\n" for x in self.sample_option_out]
        self.sample_default_out = [" A", "B", "C", "D", "E", "F",
                                   "G", "H", "i", "j"]
        self.sample_default_out = [x + "\n" for x in self.sample_default_out]
        self.sample_less_out = [" A", "B", "C", "D", "E"]
        self.sample_less_out = [x + "\n" for x in self.sample_less_out]
        self.sample_stdout = [" A", "B", "C", "D"]
        self.sample_stdout = [x + "\n" for x in self.sample_stdout]

        # lines less than 10
        with open("test/test_head_less.txt", "w") as f:
            for line in self.sample_less_in:
                f.write(line)

        # lines more than 10
        with open("test/test_head.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_head(self):
        self.app.exec(["test/test_head.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_head_less(self):
        self.app.exec(["test/test_head_less.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_less_out))

    def test_head_option(self):
        self.app.exec(["-n", "11", "test/test_head.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_option_out))

    def test_head_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec(["-n", "4"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_stdout))

    def test_head_incorrect_flag(self):
        try:
            self.app.exec(["-num", "4"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong flags")

    def test_head_no_args(self):
        try:
            self.app.exec([], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")

    def test_head_too_many_args(self):
        try:
            self.app.exec(["-n", "11", "12", "test/test_head.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")


class TestTail(unittest.TestCase):
    def setUp(self):
        from src.apps import Tail

        self.app = Tail()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = [" A", "B", "C", "D", "E", "F",
                          "G", "H", "i", "j", " are alphabet"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_less_in = [" A", "B", "C", "D", "E"]
        self.sample_less_in = [x + "\n" for x in self.sample_less_in]

        self.sample_option_out = ["j", " are alphabet"]
        self.sample_option_out = [x + "\n" for x in self.sample_option_out]
        self.sample_default_out = ["B", "C", "D", "E", "F",
                                   "G", "H", "i", "j", " are alphabet"]
        self.sample_default_out = [x + "\n" for x in self.sample_default_out]
        self.sample_less_out = [" A", "B", "C", "D", "E"]
        self.sample_less_out = [x + "\n" for x in self.sample_less_out]
        self.sample_stdout = ["H", "i", "j", " are alphabet"]
        self.sample_stdout = [x + "\n" for x in self.sample_stdout]

        # lines less than 10
        with open("test/test_tail_less.txt", "w") as f:
            for line in self.sample_less_in:
                f.write(line)

        # lines more than 10
        with open("test/test_tail.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_tail(self):
        self.app.exec(["test/test_tail.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_tail_less(self):
        self.app.exec(["test/test_tail_less.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_less_out))

    def test_tail_option(self):
        self.app.exec(["-n", "2", "test/test_tail.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_option_out))

    def test_tail_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec(["-n", "4"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_stdout))

    def test_tail_incorrect_flag(self):
        try:
            self.app.exec(["-num", "4"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong flags")

    def test_tail_no_args(self):
        try:
            self.app.exec([], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")

    def test_tail_too_many_args(self):
        try:
            self.app.exec(["-n", "2", "4", "test/test_head.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")


class TestGrep(unittest.TestCase):
    def setUp(self):
        from src.apps import Grep

        self.app = Grep()
        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_pattern = "abc"
        self.sample_in = ["abc", "Hi is bad", " abc", "Abc"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_in2 = ["abc is", "hi", " tell", "Abc"]
        self.sample_in2 = [x + "\n" for x in self.sample_in2]

        self.sample_default_out = ["abc\n"]
        self.sample_multiple_file_out = ["test/test_grep.txt:abc\n",
                                         "test/test_grep2.txt:abc is\n",
                                         ]
        self.sample_stdout = ["abc\n", " abc\n"]

        with open("test/test_grep.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)
        with open("test/test_grep2.txt", "w") as f:
            for line in self.sample_in2:
                f.write(line)

    def test_grep(self):
        self.app.exec(
            [self.sample_pattern, "test/test_grep.txt"],
            self.in_stream,
            self.out_stream
        )
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_grep_multiple_files(self):
        self.app.exec(
            [self.sample_pattern, "test/test_grep.txt", "test/test_grep2.txt"],
            self.in_stream,
            self.out_stream,
        )
        self.assertEqual(self.out_stream, deque(self.sample_multiple_file_out))

    def test_grep_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec([self.sample_pattern], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_stdout))

    def test_grep_no_args(self):
        try:
            self.app.exec([], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")


class TestUniq(unittest.TestCase):
    def setUp(self):
        from src.apps import Uniq

        self.app = Uniq()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = ["abc", "ABC", "Abc", "bat", " Ball"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_stdin = ["abc", "ABC", "Abc", "bat", " Ball"]

        self.sample_default_out = ["abc", "ABC", "Abc", "bat", " Ball"]
        self.sample_default_out = [x + "\n" for x in self.sample_default_out]
        self.sample_caseNotSensitive_out = ["abc", "bat", " Ball"]
        self.sample_caseNotSensitive_out = [
            x + "\n" for x in self.sample_caseNotSensitive_out
        ]

        with open("test/test_uniq.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_uniq(self):
        self.app.exec(["test/test_uniq.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_uniq_caseNotSensitive(self):
        self.app.exec(["-i", "test/test_uniq.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(
            self.sample_caseNotSensitive_out))

    def test_uniq_stdin(self):
        self.in_stream.extend(self.sample_stdin)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_uniq_stdin_with_option(self):
        self.in_stream.extend(self.sample_stdin)
        self.app.exec(["-i"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(
            self.sample_caseNotSensitive_out))

    def test_uniq_too_many_args(self):
        try:
            self.app.exec(["-i", "test", "test/test_uniq.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")


class TestHistory(unittest.TestCase):
    def setUp(self):
        from src.apps import History

        self.app = History()
        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_in = ["ls", "cd comp0010", "ls"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_out = ["1  ls\n",
                           "2  cd comp0010\n", "3  ls\n"]

        with open("history.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_history(self):
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_history_option(self):
        self.app.exec(["-c"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque([]))


class TestSort(unittest.TestCase):
    def setUp(self):
        from src.apps import Sort

        self.app = Sort()
        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_in = ["bat", "abc", " apple", " Abc", "BALL", "ABc", "bat"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_out = [" Abc", " apple",
                           "ABc", "BALL", "abc", "bat", "bat"]
        self.sample_out = [x + "\n" for x in self.sample_out]

        with open("./test_sort.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_sort(self):
        self.app.exec(["./test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_sort_reverse(self):
        self.app.exec(["-r", "./test_sort.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out[::-1]))

    def test_sort_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_sort_too_many_args(self):
        try:
            self.app.exec(["-r", "test", "./test_sort.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "sort: wrong number of arguments")


class TestFind(unittest.TestCase):
    def setUp(self):
        from src.apps import Find

        self.app = Find()
        self.in_stream = deque()
        self.out_stream = deque()

        filename = "find/test_find.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write("")

    def test_find_dir(self):
        self.app.exec(["find"], self.in_stream, self.out_stream)
        self.assertEqual(len(self.out_stream), 1)

    def test_find_dir_root(self):
        self.app.exec(["..", "-name", "test_find.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(
            ["../comp0010/find/test_find.txt\n"]))

    def test_find_no_dir(self):
        self.app.exec([""], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque([]))

    def test_find_name_test_find_dot_txt(self):
        self.app.exec(["-name", "test_find.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(["./find/test_find.txt\n"]))

    def test_find_name_pattern_front(self):
        self.app.exec(["-name", "*find.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(["./find/test_find.txt\n"]))

    def test_find_name_pattern_back(self):
        self.app.exec(["-name", "test_find*"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(["./find/test_find.txt\n"]))

    def test_find_name_pattern_front_back(self):
        self.app.exec(["-name", "*find*"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(
            ["./find\n", "./find/test_find.txt\n"]))

    def test_find_dir_name_pattern(self):
        self.app.exec(["find", "-name", "*.txt"],
                      self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(["find/test_find.txt\n"]))

    def test_find_no_args(self):
        try:
            self.app.exec([], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "wrong number of command line arguments")

    def test_find_one_arg_no_pattern(self):
        try:
            self.app.exec(["-name"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(str(error), "requires pattern")

    def test_find_two_args_no_pattern(self):
        try:
            self.app.exec(["find", "-name"], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(str(error), "requires pattern")

    def test_find_two_args_wrong_flag(self):
        try:
            self.app.exec(["-n", "test_find.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(str(error), "wrong flags")

    def test_find_three_args_wrong_flag(self):
        try:
            self.app.exec(["find", "-n", "test_find.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(str(error), "wrong flags")


class TestCut(unittest.TestCase):
    def setUp(self):
        from src.apps import Cut

        self.app = Cut()
        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_in = ["1 2 3 4 5", "6 7 8 9 10"]
        self.sample_in = [x + "\n" for x in self.sample_in]

        with open("./test_cut.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_cut_no_range(self):
        self.app.exec(["-b", "2,3", "./test_cut.txt"],
                      self.in_stream, self.out_stream)
        expected = [" 2\n", " 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_no_range_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec(["-b", "2,3"], self.in_stream, self.out_stream)
        expected = [" 2\n", " 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_one_close_range(self):
        self.app.exec(["-b", "2-3", "./test_cut.txt"],
                      self.in_stream, self.out_stream)
        expected = [" 2\n", " 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_two_close_ranges(self):
        self.app.exec(
            ["-b", "2-3,4-5", "./test_cut.txt"],
            self.in_stream, self.out_stream)
        expected = [" 2 3\n", " 7 8\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_one_open_range(self):
        self.app.exec(["-b", "2-", "./test_cut.txt"],
                      self.in_stream, self.out_stream)
        expected = [" 2 3 4 5\n", " 7 8 9 10\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_first_is_open(self):
        self.app.exec(["-b", "-3", "./test_cut.txt"],
                      self.in_stream, self.out_stream)
        expected = ["1 2\n", "6 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_two_open_ranges(self):
        self.app.exec(
            ["-b", "2-,4-", "./test_cut.txt"], self.in_stream, self.out_stream
        )
        expected = [" 2 3 4 5\n", " 7 8 9 10\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_one_close_one_open_range(self):
        self.app.exec(
            ["-b", "2-3,4-", "./test_cut.txt"], self.in_stream, self.out_stream
        )
        expected = [" 2 3 4 5\n", " 7 8 9 10\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_empty_search(self):
        self.app.exec(
            ["-b", "3-1", "./test_cut.txt"],
            self.in_stream,
            self.out_stream
        )
        expected = ["\n", "\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_incorrect_flag(self):
        try:
            self.app.exec(["-r", "1-3", "./test_cut.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "Invalid option")

    def test_cut_few_args(self):
        try:
            self.app.exec([], self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "Invalid number of arguments")

    def test_cut_too_many_args(self):
        try:
            self.app.exec(["-b", "1-3", "4-5", "./test_cut.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "Invalid number of arguments")

    def test_cut_no_byte_range(self):
        try:
            self.app.exec(["-b", "-", "./test_cut.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "Invalid range")

    def test_cut_invalid_byte_range(self):
        try:
            self.app.exec(["-b", "1-2-3", "./test_cut.txt"],
                          self.in_stream, self.out_stream)
        except ValueError as error:
            self.assertEqual(
                str(error), "Invalid input")


class TestCall(unittest.TestCase):
    def setUp(self):

        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_in1 = ["hello", "world"]
        self.sample_in1 = [x + "\n" for x in self.sample_in1]
        self.sample_in2 = ["foo", "bar"]
        self.sample_in2 = [x + "\n" for x in self.sample_in2]
        self.sample_out = ["hello", "world", "foo", "bar"]
        self.sample_out = [x + "\n" for x in self.sample_out]

        filename = "call/"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open("call/test_call1.txt", "w") as f:
            for line in self.sample_in1:
                f.write(line)

        with open("call/test_call2.txt", "w") as f:
            for line in self.sample_in2:
                f.write(line)

    def test_call_no_globbing(self):
        from commands import Call
        call = Call('echo', ['foo'])
        call.eval(self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(['foo\n']))

    def test_call_include_globbing(self):
        from commands import Call
        call = Call('cat', ['call/*.txt'])
        call.eval(self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


class TestSequence(unittest.TestCase):
    def setUp(self):
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = ["hello", "world"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_out = ["foo", "hello", "world"]
        self.sample_out = [x + "\n" for x in self.sample_out]

        with open("test/test_sequence.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_sequence(self):
        from commands import Call, Sequence
        app1 = Call('echo', ['foo'])
        app2 = Call('cat', ["test/test_sequence.txt"])
        seq = Sequence(app1, app2)

        seq.eval(self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


class TestPipe(unittest.TestCase):
    def setUp(self):
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = ["foo", "bar"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_out = ["foo"]
        self.sample_out = [x + "\n" for x in self.sample_out]

        with open("test/test_pipe.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_pipe(self):
        from commands import Call, Pipe
        app1 = Call('cat', ["test/test_pipe.txt"])
        app2 = Call('grep', ["foo"])
        pipe = Pipe(app1, app2)

        pipe.eval(self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


class TestUnsafeDecorator(unittest.TestCase):
    def setUp(self):
        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_out = ["wrong number of command line arguments"]
        self.sample_out = [x + "\n" for x in self.sample_out]

    def test_unsafe_decorato_with_no_error(self):
        from commands import Call
        call = Call('_echo', ['foo'])
        call.eval(self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(['foo\n']))

    def test_unsafe_decorator_with_error(self):
        from commands import Call
        call = Call('_ls', ['foo', 'bar'])
        call.eval(self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.in_stream = deque()
        self.out_stream = deque()

    def test_application_unknown_app(self):
        from apps import Application
        try:
            Application.by_name("foo")
        except ValueError as error:
            self.assertEqual(str(error), "Unknown application: foo")

    from apps import Application

    @patch.multiple(Application, __abstractmethods__=set())
    def test_application_not_implemented(self):
        from apps import Application
        app = Application()
        try:
            app.exec([], self.in_stream, self.out_stream)
        except NotImplementedError as error:
            self.assertEqual(str(error), '')


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.in_stream = deque()
        self.out_stream = deque()

    from commands import Command

    @patch.multiple(Command, __abstractmethods__=set())
    def test_application_not_implemented(self):
        from commands import Command
        command = Command()
        try:
            command.eval(self.in_stream, self.out_stream)
        except NotImplementedError as error:
            self.assertEqual(str(error), '')


if __name__ == "__main__":
    unittest.main()
