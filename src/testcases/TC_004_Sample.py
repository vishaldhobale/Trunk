import os
import sys
import unittest

sys.path.append(os.getcwd())

def add(x, y):
    return x + y


class SimpleTest(unittest.TestCase):
    def runTest(self):
        self.test_id = "TC_004"
        self.test_name = "Test addition of two number"
        self.server_type = "S4"
        self.test_flg = 1
        self.assertEqual(add(4, 5), 9)


if __name__ == "__main__":
    unittest.main()
