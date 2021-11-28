import io
import pathlib
import collections
from pathlib import Path
import unittest
import os

# 与文件相关的各种操作在 os.path 里提供了各种方法；
# 在 3.4.0 之后，建议使用 pathlib.Path 操作目录和文件，使用更方便
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

    def test_get_current_work_dir(self):
        """测试获取当前工作目录的几种方式以及相互之间的比较
        """
        # 获得当前工作目录
        p1 = Path.cwd()  # Output: PosixPath('/Users/ktgu/workspace/projects/python-demos')

        # 使用构造函数传入空字符串或 '.' 表示的也是当前工作目录
        # 只是他们返回的是相对路径
        p2 = Path()  # PosixPath('.')
        p3 = Path('.') # PosixPath('.')

        # repr 和 str 输出的字符是不一样的，repr 更具表达性
        self.assertEqual("PosixPath('.')", repr(p2))
        self.assertEqual(".", str(p2))

        # 断言：p2,p3 都是相对路径
        self.assertFalse(p2.is_absolute())
        self.assertFalse(p3.is_absolute())

        # 两个表示同一个路径的相对地址比较是相等的，但是表示同一个目录的相对路径和绝对的路径比较是不等的
        self.assertEqual(p2, p3)
        self.assertNotEqual(p2, p1)
        # 但是转换为绝对地址就可以比较了
        self.assertEqual(p1, p2.absolute())

    def test_get_user_home_dir(self):
        """获取用户 home 目录"""
        # 调用类方法 home,构造用户的 home dir 路径实例
        p1 = Path.home()  # PosixPath('/Users/ktgu')
        # 该方法是通过 os.path.expanduser('~') 返回的，但是该方法返回值是 str 类型
        p2 = os.path.expanduser('~')
        self.assertEqual('/Users/ktgu', p2)

        # 虽然两个指向的路径系统，但两个变量的类型不同
        self.assertNotEqual(p1, p2)
        # 如果要比较，需要将类型转换一致
        self.assertEqual(p1, Path(p2))

    def test_get_path_base_user_home_dir(self):
        """获取基于 user home 的路径

        关于 expanduser 方法的说明，可执行 help(Path.expanduser) 查看帮助
        expanduser() method of pathlib.PosixPath instance
        Return a new path with expanded ~ and ~user constructs
        (as returned by os.path.expanduser)
        """
        self.assertEqual('/Users/ktgu/.ssh', Path('~/.ssh').expanduser())

    def test_iter_dirs(self):
        """遍历指定目录下的所有文件及目录"""
        for path in Path.home().iterdir():
            print(path)

        # Path.home().iterdir() 是一个 collections.generator
        self.assertIs(collections.generator, type(Path.home().iterdir()))

    def test_get_file_suffix(self):
        """获取文件后缀名（扩展名）
        """
        # suffix 属性返回最后一个.的扩展名
        self.assertEqual('.gz', Path('1.tar.gz').suffix)
        # suffixes 属性返回多个扩展名列表
        self.assertEqual(['.tar', '.gz'], Path('1.tar.gz').suffixes)

        # with_suffix 可以修改后缀名，返回一个新实例，不影响原实例后缀名
        p1 = Path('1.md')

    def test_change_file_name_or_suffix(self):
        """测试更改文件名或扩展名
        """
        p1 = Path('1.md')
        p2 = p1.with_suffix('.txt')

        self.assertNotEqual(p1, p2)
        print(repr(p1), repr(p2))  # Output: PosixPath('1.md') PosixPath('1.txt')

        # 修改文件名（不包含扩展名）
        p3 = p1.with_stem('foo')
        self.assertEqual('foo.md', str(p3))

        # 和 with_suffix 相对的是 with_name, 用以修改文件名
        p4 = p1.with_name('bar')
        self.assertEqual('bar', str(p4))

    def test_get_part_of_path(self):
        """取路径的各个部分


        本测试用例将用到以下属性：
        name: 获取目录或文件名（包括扩展名）
        suffix: 获取最后一个后缀名，如 1.tar.gz 返回 .gz
        suffixes: 获取所有后缀名 list，如 1.tar.gz 返回 ['.tar', '.gz']
        stem: 获取除最后一个后缀名以外的文件名部分，如 1.tar.gz 返回 1.tar
        parent: 获取 stem 父路径
        parents: 返回一个类似序列的对象 <class 'pathlib._PathParents'>，通过它可以迭代所有前置路径
        """
        # 创建一个 Path 实例，此处使用绝对路径方便后面解释 parent 和 parents 属性
        p = Path('1.tar.gz').absolute()
        self.assertEqual('/Users/ktgu/workspace/projects/python-demos/1.tar.gz', str(p))

        # 获取目录或文件名(包括扩展名）
        self.assertEqual('1.tar.gz', p.name)
        # 获取不带扩展名的文件或目录名
        self.assertEqual('1.tar', p.stem)
        # 获取最后一个.表明的扩展名，此处输出.gz
        self.assertEqual('.gz', p.suffix)
        # 如果类似像 1.tar.gz 这种有两个点分隔的，该属性会返回一个扩展名列表
        self.assertEqual( ['.tar', '.gz'], p.suffixes)

        # 获取父路径
        self.assertEqual('/Users/ktgu/workspace/projects/python-demos', str(p.parent))

        # 遍历 parents
        # Output：
        # /Users/ktgu/workspace/projects/python-demos
        # /Users/ktgu/workspace/projects
        # /Users/ktgu/workspace
        # /Users/ktgu
        # /Users
        # /
        for path in p.parents:
            print(path)

    def test_path_exists(self):
        """测试路径是否存在
        """
        p1 = Path('1.md')

        # 断言：路径是否存在
        self.assertTrue(p1.exists())
        self.assertTrue(os.path.exists('1.md'))

    def test_path_is_file_or_dir(self):
        """测试路径是否是文件或目录
        """
        p1 = Path('1.md')

        # 断言：是一个文件
        self.assertTrue(Path('1.md').is_file())
        self.assertTrue(os.path.isfile('1.md'))

        # 断言：不是文件夹
        self.assertFalse(p1.is_dir())
        self.assertFalse(os.path.isdir('1.md'))

    def test_path_join(self):
        # 使用 pathlib.Path
        path1 = Path('/usr', 'local', 'bin')
        self.assertEqual('/usr/local/bin', str(path1))

        path2 = os.path.join('/usr', 'local', 'bin')
        self.assertEqual('/usr/local/bin', path2)

    def test_fifo_file(self):
        # TODO
        pass

    def test_mkdir_or_create_new_file(self):
        # TODO
        # 创建一个新文件
        Path('2.md').touch()

    def test_as_file_url(self):
        """测试将路径返回为 'file' URI（file://...的形式）
        """
        p1 = Path('1.md')
        # as_uri 只能在绝对路径上调用，否则会发生 ValueError
        # ValueError: relative path can't be expressed as a file URI
        with self.assertRaises(ValueError):
            print(p1.as_uri())
        # 只有绝对路径才可以转换为 file URI
        self.assertEqual('file:///Users/ktgu/workspace/projects/python-demos/1.md', p1.absolute().as_uri())

    def test_file_commons(self):
        file_name = '1.md'
        p1 = Path(file_name)

        # TODO

        # 是否是块设备
        p1.is_block_device()
        # 是否是字符设备
        p1.is_char_device()
        # 是否是 FIFO 管道文件
        p1.is_fifo()
        # 是否是软连接
        p1.is_symlink()
        # 是否是socket文件
        p1.is_socket()
        # 是否是绝对路径
        p1.is_absolute()
        # 是否是挂载点
        p1.is_mount()

        # path.chmod(777)
        # path.is_relative_to()
        p1.is_reserved()
        p1.anchor
        p1.drive
        p1.open()
        p1.root()
        p1.stat()
        p1.with_stem()
        # os.stat_result(st_mode=33188, st_ino=8722088793, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=11,
        #                st_atime=1638094154, st_mtime=1638094151, st_ctime=1638094151)


if __name__ == '__main__':
    unittest.main()
