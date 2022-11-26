import unittest
import os

from collections import deque


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
        self.sample_multiple_file_out = [
            "test/test_grep.txt:abc\n",
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
            x + "\n" for x in self.sample_caseNotSensitive_out]

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
            self.in_stream,
            self.out_stream
        )
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


if __name__ == "__main__":
    unittest.main()
