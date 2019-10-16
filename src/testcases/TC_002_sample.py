import unittest


def sub(x, y):
    return x - y


class SimpleTest(unittest.TestCase):
    def runTest(self):
        self.test_id = "TC_001"
        self.test_name = "Test subtraction of two number"
        self.server_type = "S2"
        self.test_flg = 1
        self.assertEqual(sub(5, 4), 1)


if __name__ == "__main__":
    unittest.main()
