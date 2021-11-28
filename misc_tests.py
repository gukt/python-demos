import unittest
import math
import operator

class Foo:

    def __int__(self):
        return 1

    def __float__(self):
        return 1.0

    def __complex__(self):
        return 3+4j

    def __index__(self):
        return 3

class MyTestCase(unittest.TestCase):

    @staticmethod
    def test_loop1():
        params = {'name': 'foo', 'password': 'bar'}
        for k, v in params.items():
            print(k, v)

    def test_math(self):
        a, b = 1, 2
        print(a, b)
        assert 5 / 2 == 2.5
        assert 5 // 2 == 2
        assert 5
        assert isinstance(1, int)
        assert not issubclass(int, str)

    def test_special_methods(self):
        print('test_special_methods')
        foo = Foo()
        lst = list('hello')
        print(lst[0: foo])
        assert 1 == int(foo)
        assert 1.0 == float(foo)

        d1 = {'foo': 'bar', 123: 456}
        d1.setdefault('zoo', 'bear')
        dict


if __name__ == '__main__':
    unittest.main()
