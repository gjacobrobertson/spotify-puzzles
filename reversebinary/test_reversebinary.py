import unittest
import reversebinary
import random
import sys


class TestReverseBinary(unittest.TestCase):
    def test_reverse_num(self):
        self.assertEqual(reversebinary.reverse_num(1), 1)
        self.assertEqual(reversebinary.reverse_num(2), 1)
        self.assertEqual(reversebinary.reverse_num(1000000000), 1365623)

        for i in range(1000):
            num = random.randint(1, 1000000000)
            rnum = reversebinary.reverse_num(num)
            num_bin = bin(num)[2:]
            rnum_bin = bin(rnum)[2:].zfill(len(num_bin))
            self.assertEqual(num_bin, rnum_bin[::-1])


if __name__ == '__main__':
    unittest.main()
