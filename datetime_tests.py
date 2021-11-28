import unittest

from datetime import date, time, datetime, timedelta


# TODO datetime.now() 和  datetime.today() 的区别
# TODO
#
class DateTimeTest(unittest.TestCase):

    @staticmethod
    def test_dateime():
        now = datetime.now()

        # Output: 2021-11-24 17:41:24.700623
        print(now)
        # 打印年/月/日/时/分/秒/微秒
        # Output: 2021 11 24 17 41 24 700623
        print(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
        # 没有提供毫秒属性，可通过计算获得
        # Output: 700
        print(now.microsecond // 1000)

        # NOTE: min 属性不是表示分钟，而是 datetime 可表示的最小时间；max 是可表示的最大时间
        # Output: 0001-01-01 00:00:00, 9999-12-31 23:59:59.999999
        print(now.min, now.max, sep=', ')

        print(now.utcnow())
        print(datetime.utcnow())

        date.today()
        datetime.today()
        datetime.now()


# 入口函数
if __name__ == '__main__':
    unittest.main()
