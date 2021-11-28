import unittest
from redis import Redis, ConnectionPool


class RedisTests(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

    def test_connection(self):
        """测试连接本地 redis 服务器，然后写入一个 string 类型的 key 并读取出来"""
        # Redis 构造函数默认值：host=localhost, port=6379, db=0
        # 等效于: redis = Redis()
        redis = Redis(host='localhost', port=6379, db=0)
        redis.set('s1', 'hello')
        print(redis.get('s1'))  # Output: b'hello'

    def test_connection_pool(self):
        pool = ConnectionPool(host='localhost', port=6379)
        redis = Redis(connection_pool=pool)
        redis.set('s1', 'hello')
        print(redis.get('s1'))  # Output: b'hello'

if __name__ == '__main__':
    unittest.main()
