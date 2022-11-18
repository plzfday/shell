import unittest

from collections import deque


class TestSort(unittest.TestCase):
    def setUp(self):
        from src.apps import Sort

        self.app = Sort()
        self.in_stream = deque()
        self.out_stream = deque()
        self.sample_in = ["bat", "abc", " apple", " Abc", "BALL", "ABc", "bat"]
        self.sample_default_out = [" Abc", " apple", "ABc", "BALL", "abc", "bat", "bat"]

        with open("test/test_sort.txt", "w") as f:
            for line in self.sample_in:
                f.write(line + "\n")

    def test_sort(self):
        self.app.exec(["test/test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))

    def test_sort_reverse(self):
        self.app.exec(["-r", "test/test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out[::-1]))

    def test_sort_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_default_out))


if __name__ == "__main__":
    unittest.main()
