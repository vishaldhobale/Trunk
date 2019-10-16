import unittest


def multiplication(x, y):
    return x * y


class SimpleTest(unittest.TestCase):
    def runTest(self):
        self.test_id = "TC_003"
        self.test_name = "Test substraction of two number"
        self.server_type = "S3"
        self.test_flg = 1
        self.assertEqual(multiplication(4, 5), 45)


if __name__ == "__main__":
    unittest.main()
