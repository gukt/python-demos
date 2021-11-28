import json
import unittest
import pathlib


def _ensure_file(name: str):
    """确保指定的文件存在，如果不存在则创建一个"""
    path = pathlib.Path(name)
    if not path.exists():
        path.touch()


class JsonTests(unittest.TestCase):
    """JSON 相关测试案例"""

    def test_json_dumps_and_loads(self):
        d1 = dict(one=1, two=2, three=3)
        # 将 dict 对象序列化为 json 字符串
        s = json.dumps(d1)
        self.assertEqual('{"one": 1, "two": 2, "three": 3}', s)

        # 再将 json 字符串转换为 dict 对象
        d2 = json.loads(s)
        self.assertEqual(d1, d2)

        # 两个实例内容一样，但不是同一个实例
        self.assertIsNot(d1, d2)

        # 也可以将 list, tuple 等转换为 json 对象
        self.assertEqual('[1, 2, 3]', json.dumps((1, 2, 3,)))
        self.assertEqual('[1, 2, 3]', json.dumps([1, 2, 3]))

        # 不支持对 range 对象的序列化
        # TypeError: Object of type set is not JSON serializable
        with self.assertRaises(TypeError):
            json.dumps(range(10))
        # 可以将其先转变为 list 或 tuple 再序列化
        self.assertEqual('[1, 2, 3]', json.dumps(list(range(1, 4))))

    def test_dump_to_file(self):
        """测试使用 json.dump 方法将序列化的结果直接保存到文件中。
        """
        d1 = dict(one=1, two=2, three=3)
        # dumps 还有个变体 dump，它将序列化的内容写入文件
        _ensure_file('1.json')
        # 设置文件为可读写，以便后面将序列化的内容写入，然后读出内容用于断言
        f = open('1.json', 'w+')
        json.dump(d1, f)
        f.seek(0)
        self.assertEqual('{"one": 1, "two": 2, "three": 3}', f.read())

    def test_load_from_file(self):
        """测试使用 json.load 方法从文件中读取 JSON 字符串，并将其序列化为对象。
        """
        f = open('1.json')
        # 同 dump 方法一样，load 方法用以从文件中读取内容并序列化为对象
        obj = json.load(f)
        self.assertIsNotNone(obj)
        self.assertIs(dict, type(obj))


if __name__ == '__main__':
    unittest.main()
