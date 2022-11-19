import unittest

from collections import deque


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

        with open("./test_sort.txt", "w") as f:
            for line in self.sample_in:
                f.write(line)

    def test_sort(self):
        self.app.exec(["./test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))

    def test_sort_reverse(self):
        self.app.exec(["-r", "./test_sort.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out[::-1]))

    def test_sort_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec([], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(self.sample_out))


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
        self.app.exec(["-b", "2,3", "./test_cut.txt"], self.in_stream, self.out_stream)
        expected = [" 2\n", " 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_no_range_stdin(self):
        self.in_stream.extend(self.sample_in)
        self.app.exec(["-b", "2,3"], self.in_stream, self.out_stream)
        expected = [" 2\n", " 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_one_close_range(self):
        self.app.exec(["-b", "2-3", "./test_cut.txt"], self.in_stream, self.out_stream)
        expected = [" 2\n", " 7\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_two_close_ranges(self):
        self.app.exec(
            ["-b", "2-3,4-5", "./test_cut.txt"], self.in_stream, self.out_stream
        )
        expected = [" 2 3\n", " 7 8\n"]
        self.assertEqual(self.out_stream, deque(expected))

    def test_cut_one_open_range(self):
        self.app.exec(["-b", "2-", "./test_cut.txt"], self.in_stream, self.out_stream)
        expected = [" 2 3 4 5\n", " 7 8 9 10\n"]
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


if __name__ == "__main__":
    unittest.main()
