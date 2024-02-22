import requests
from bs4 import BeautifulSoup

def key_user_input():
    key_user_input = input("请输入你的卡密:")
    return key_user_input

def key():
    response = requests.get("https://github.com/xiexiaozhua/xiexiaozhua/blob/main/index.html")
    soup = BeautifulSoup(response.text, 'lxml')
    # 假设卡密是在某个特定的HTML元素中，例如<pre>或者<p>标签，这里需要根据实际情况修改
    # 下面的代码以<pre>标签为例
    key_text = soup.find('pre').text  # 修改这里以匹配实际的HTML结构
    return key_text

user_input = key_user_input()
key_content = key()  # 获取处理后的卡密文本
if len(user_input) > 32 and user_input in key_content:
    print("1")
else:
    print("2")
