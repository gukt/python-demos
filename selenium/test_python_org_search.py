import tracemalloc
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# 定义一个测试类，继承自 unittest.TestCase，告诉 unittest 模块，该类是一个测试用例
class PythonOrgSearch(unittest.TestCase):

    # 该方法会在该测试类中的每一个测试方法被执行前都执行一遍
    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=Service(executable_path='/usr/local/chromedriver'))

    # 定义一个测试方法，始终以 test 开头
    def test_search_in_pytahon_org(self):
        driver = self.driver
        driver.get("https://www.python.org")
        # 断言：标题中是否含有 Python 字符串
        self.assertIn('Python', driver.title)
        elem = driver.find_element(By.NAME, 'q')
        elem.clear()
        elem.send_keys('quickstart')
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    # 该方法会在每一个测试方法执行之后被执行，一般用来做一些清扫工作，比如关闭浏览器
    def tearDown(self) -> None:
        self.driver.close()


# 入口函数
if __name__ == '__main__':
    unittest.main()
