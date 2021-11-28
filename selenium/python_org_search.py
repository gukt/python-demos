from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 创建一个 chrome driver 实例
# NOTE: 这种用法已经过时了: driver = webdriver.Chrome(executable_path='/usr/local/chromedriver')
driver = webdriver.Chrome(service=Service(executable_path='/usr/local/chromedriver'))

# 打开网站， WebDriver 会等待整个页面加载完成（其实是等待”onload”事件执行完毕）之后才把控制权交给测试程序
# 如果你的页面使用大量的AJAX技术来加载页面，WebDriver可能不知道什么时候页面已经加载完成
driver.get("https://www.python.org")
# 打印网页源码
# print(driver.page_source)
# 打印网页标题
# print(driver.title)
# 断言: 标题中含有 Python 字符串
assert 'Python' in driver.title

# 通过元素名称获取元素
# NOTE: 旧的用法是 find_element_by_name，不过新版本里 find_element_* 都被弃用了，统一使用 find_element 函数
elem = driver.find_element(By.NAME, 'q')
# 因为 send_keys 函数是不会清除输入框中原有值的，它会将内容添加到已有内容之后
# 所以，这里用 clear 将输入框内容先清空
elem.clear()
# 输入 'quickstart' 关键字
elem.send_keys('quickstart')
# 回车，也可以使用 Keys.ENTER
# 不过，真正的回车键应该叫 RETURN，小键盘上那个才是 Enter 键
# Enter 键是 PC 习惯，MAC 上的回车键上既有 Enter 又有 Return 字符标记
elem.send_keys(Keys.RETURN)
# 断言：搜索结果中有满足条件的内容
assert "No results found." not in driver.page_source

# 添加 cookie
driver.add_cookie({'name': 'foo', 'value': 'bar'})
# 打印所有 cookies
print('cookies:\n', driver.get_cookies())

# 浏览历史后退一步。前进用 forward()
# 请注意，这个功能完全取决于底层驱动程序。当你调用这些方法的时候，很有可能会发生意想不到的事情。
driver.back()

# TODO 等待 3 秒
# print(elem)
# driver.close()
