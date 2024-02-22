from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 指定Microsoft Edge浏览器驱动的路径（请替换成你下载的驱动路径）
edge_driver_path = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # 替换为实际路径

# 创建EdgeOptions对象
edge_options = webdriver.EdgeOptions()

# 创建一个Edge浏览器实例，通过executable_path参数传递EdgeDriver路径
driver = webdriver.Edge(executable_path=edge_driver_path, options=edge_options)

# 打开网页
url = 'https://www.bilibili.com'
driver.get(url)

# 添加等待，等待元素出现在DOM中并且可见
try:
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "a"))
    )

    # 执行点击操作
    element.click()
except Exception as e:
    print(f"Error: {e}")

# 执行完操作后，可以关闭浏览器
driver.quit()
