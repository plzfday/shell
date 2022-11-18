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

class TestFind(unittest.TestCase):
    def setUp(self):
        from src.apps import Find
        self.app = Find()
        self.in_stream = deque()
        self.out_stream = deque()

        with open("test/test_find.txt", "w") as f:
            f.write("")

    def test_find_dir(self):
        self.app.exec(["test"], self.in_stream, self.out_stream)
        self.assertEqual(len(self.out_stream), 3)

    def test_find_name_test_file_dot_txt(self):
        self.app.exec(["-name", "test_find.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(["./test/test_find.txt\n"]))

    def test_find_name_pattern(self):
        self.app.exec(["-name", "*.txt"], self.in_stream, self.out_stream)
        self.assertEqual(len(self.out_stream), 7)

    def test_find_dir_name_pattern(self):
        self.app.exec(["test", "-name", "*.txt"], self.in_stream, self.out_stream)
        self.assertEqual(self.out_stream, deque(["test/test_find.txt\n"]))

if __name__ == "__main__":
    unittest.main()
