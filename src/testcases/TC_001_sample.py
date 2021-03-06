import os
import sys
import time
import unittest


sys.path.append(os.getcwd())


def add(x, y):
    return x + y


class SimpleTest(unittest.TestCase):
    def runTest(self):
        self.test_id = "TC_001"
        self.test_name = "Test addition of two number"
        self.server_type = "S1"
        self.test_flg = 1
        self.assertEqual(add(4, 5), 9)


if __name__ == "__main__":
    unittest.main()
