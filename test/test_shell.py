import unittest

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
            [self.sample_pattern, "test/test_grep.txt"], self.in_stream, self.out_stream
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
        self.sample_caseNotSensitive_out = [x + "\n" for x in self.sample_caseNotSensitive_out]
        
        


        with open("test/test_uniq.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_uniq(self):
        self.app.exec(["test/test_uniq.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_uniq_caseNotSensitive(self):
        self.app.exec(["-i", "test/test_uniq.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_caseNotSensitive_out))

    def test_uniq_stdin(self):
        self.in_stream.extend(self.sample_stdin)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_uniq_stdin_with_option(self):
        self.in_stream.extend(self.sample_stdin)
        self.app.exec(["-i"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_caseNotSensitive_out))


class TestSort(unittest.TestCase):
    def setUp(self):
        from src.apps import Sort

        self.app = Sort()
        self.in_stream = deque()
        self.out_stream = deque()

        self.sample_in = ["bat", "abc", " apple", " Abc", "BALL", "ABc", "bat"]
        self.sample_in = [x + "\n" for x in self.sample_in]
        self.sample_out = [" Abc", " apple", "ABc", "BALL", "abc", "bat", "bat"]
        self.sample_out = [x + "\n" for x in self.sample_out]

        with open("test/test_sort.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_sort(self):
        self.app.exec(["test/test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_sort_reverse(self):
        self.app.exec(["-r", "test/test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out[::-1]))

    def test_sort_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


if __name__ == "__main__":
    unittest.main()
