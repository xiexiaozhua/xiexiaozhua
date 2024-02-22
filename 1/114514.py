from selenium.webdriver.common.keys import Keys

# 假设 driver 已经打开了网页

# 定位输入框元素
input_element = driver.find_element_by_class_name("nav-search-input")

# 点击输入框
input_element.click()

# 输入指定内容
input_element.send_keys("你的指定内容")

# 可以使用 Keys.RETURN 模拟按下回车键
input_element.send_keys(Keys.RETURN)
