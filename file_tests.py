import io
import unittest

# 可以通过内置的 open 函数来访问文件，该函数返回一个 file object 对象（<class '_io.TextIOWrapper'>）
class FileTests(unittest.TestCase):

    # 该方法会在该测试类中的每一个测试方法被执行前都执行一遍
    def setUp(self) -> None:
        """为每个测试用例准备相同的文件内容：hello\nworld"""
        f = open('1.md', 'w')
        f.write('hello\nworld')

    def test_reading_file(self):
        """测试读取文件内容；使用 seek 重新定位文件对象位置"""
        # 假设 1.md 文件完整内容为：hello\nworld
        f = open('1.md')

        # 读取完整的文件内容
        self.assertEqual('hello\nworld', f.read())
        # 再次读取会输出空字符串，因此此时读指针指向了文件末尾
        self.assertEqual('', f.read())

        # 使用 tell 方法可以告诉我们文件对象在文件中的当前位置
        self.assertEqual(11, f.tell())

        # 如果想重新读取，可以调用 seek 方法将指针指向文件头
        # 也可以指定读取多少个字符
        f.seek(0)
        self.assertEqual('hello', f.read(5))

    def test_writing_file(self):
        # open 函数的第二个参数 mode 用以指定各种模式组合：
        # r: （默认）只读方式打开，文件只能读不能写；打开文件后文件对象位于文件开头
        # r+: 读写模式，不清空文件内容
        # w: 写入模式，清空文件内容
        # w+: 读写模式，清空文件内容（注意和 r+ 的区别在于是否清空文件内容）
        # a: 追加模式，任何写入的内容会被追加到文件原内容之后，不清空文件内容；打开文件后文件对象位于文件结尾
        # a+: 追加模式+可读，注意：打开后文件对象位于文件结尾，而 r 模式位于开头。
        # 关于 mode 的使用总结：
        # 主要根据操作目的，选择适合的 mode，如果想要截断（丢弃）原内容，则使用 w 而不是 a
        # 如果修改后还需要读，则加上 +，即：w+ 或 a+
        # 选择 w+ 或 a+ 的区别在于是否要覆盖写入还是追加写入
        # 另外，追加模式的 write 方法不受 seek 方法重新定位的影响会始终在末尾追加，而 r+ 或 w+ 会在当前位置写
        # 如果既不是覆盖写入也不是追加写入，而是要保留原文件内容的情况下，修改某些地方的内容，则使用 r+。

        # 以覆盖写入模式打开文件
        f = open('1.md', 'w')

        # 源文件内容会被清空，所以这里 tell 方法会返回 0
        self.assertEqual(0, f.tell())
        # 写入两个中文字符，返回值为成功写入字符的个数
        n = f.write('你好')  # Output: 2
        self.assertEqual(2, n)
        # 注意，tell 方法返回的并不是字符个数，而是字节个数
        self.assertEqual(6, f.tell())
        # 可以多次写入
        f.write('世界')  # Output: 2
        self.assertEqual(12, f.tell())

        # 因为模式是 'w'，所以当前不可以读，
        # 先要读写，请考虑使用 r+ 或 w+ 或 a+
        # 断言：f.read 会引发 io.UnsupportedOperation: not readable 异常
        with self.assertRaises(io.UnsupportedOperation):
            f.read()

        # 如果想要可读写，请考虑使用 'r+'、'w+' 或 'a+'，取决于你是否需要清空文件原内容
        f = open('1.md', 'w+')
        # 输出 0，表示指向文件开头
        self.assertEqual(0, f.tell())
        # 输出 0，表示内容为空，因为模式设置为了 w+，所以此处可以读取了
        self.assertEqual('', f.read())
        f.write('你好')
        self.assertEqual(6, f.tell())
        # 将读指针指向头部
        f.seek(0)
        self.assertEqual('你好', f.read())
        # 再次指向头部
        f.seek(0)
        f.write('世界')
        f.seek(0)
        # 发现，内容中的'你好'被'世界'覆盖了，所以 w+ 模式下的写，受当前位置的影响
        # 而 a+ 模式下，连续多次调用 write 方法写入内容，不管中间如何调用 seek 移动指针，内容始终被追加到末尾（请自行测试）
        self.assertEqual('世界', f.read())

    def test_write_lines(self):
        f = open('1.md', 'w+')
        # 可以传入 list，一次写入多个内容，注意：行结尾分隔符不会自动添加，需要自己在待写入内容中指定
        f.writelines(['hello', 'world'])
        f.seek(0)
        self.assertEqual('helloworld', f.read())

    def test_seeking(self):
        # 使用 seekable 方法判断文件是否支持随机访问，
        # 如果返回 false，则 seek(), tell(), truncate() 方法将返回 OSError
        f = open('1.md', 'r')
        self.assertTrue(f.seekable())

        # seek 方法用于改变流位置，有两个参数指定，第一个是 offset 用以指定偏移的字节数，
        # offset 参数依赖于第二个参数 whence：
        # 0 - 流的开始位置（默认），offset 必须是 0 或正整数
        # 1 - 当前流位置，offset 可以为负数
        # 2 - 流的结尾，offset 通常为负值
        # NOTE: 以文本文件模式打开的（不是 b 模式）文件，只能基于文件开头，即 whence 只能为 0，不能设置为 1 或 2
        f = open('1.md', 'r')
        f.seek(6)
        self.assertEqual('world', f.read())
        # 因为是文件模式打开的，whence 只能从文件头开始
        # io.UnsupportedOperation: can't do nonzero end-relative seeks
        with self.assertRaises(io.UnsupportedOperation):
            f.seek(-2, 2)

        f = open('1.md', 'w')
        f.write('你好，世界')
        f = open('1.md', 'rb')
        # 以流结尾为参考点，偏移 3 个字节，注意：这里要填负数
        f.seek(-3, 2)
        self.assertEqual('界', str(f.readline(), 'utf-8'))

    def test_reading_lines(self):
        f = open('1.md')
        # 可以逐行读取
        self.assertEqual('hello\n', f.readline())
        self.assertEqual('world', f.readline())
        self.assertEqual('', f.readline())

        # 也可以一次读取所有行，返回值类型为 list
        f.seek(0)
        self.assertEqual(['hello\n', 'world'], f.readlines())
        self.assertIs(list, type(f.readlines()))

        # f.readlines() 等效于使用 list(f)
        self.assertEqual(f.readlines(), list(f))
        # print(list(f))  # Output: ['hello\n', 'world\n']

    def test_iter_lines(self):
        f = open('1.md')

        # file object 是可迭代的
        self.assertIsNotNone(f.__iter__())

        # 直接在 file object 上迭代，这种方式效率最高，因为不会存在中介变量而耗费内存
        for line in f:
            print(line)

        # 当然，你也可以在返回的 list 类型结果上迭代，但这样会消耗更多的内存，对于大文件不建议使用
        # 因为文件内容被预先读取并保存到一个 list 类型变量里了
        for line in f.readline():
            print(line)
        # 前面提到过 list(f) 等效于 f.readline()，所以也可以见到以下这样的写法
        for line in list(f):
            print(line)


if __name__ == '__main__':
    unittest.main()
