import unittest

from generators.java.enum import Enum


class TestEnum(unittest.TestCase):
    def test_enum(self):
        v = Enum("com.susamn.SusamEnum")
        v.add_enum("A")
        v.add_enum("B")
        v.add_enum("C")
        v.generate(4)


if __name__ == '__main__':
    unittest.main()
