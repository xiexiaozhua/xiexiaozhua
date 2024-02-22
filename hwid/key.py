import requests
import time
def key_user_input():
    key_user_input = input("请输入你的卡密:")
    return key_user_input

def key():
    key = requests.get("https://github.com/xiexiaozhua/xiexiaozhua/blob/main/key.html").text
    return key

user_input = key_user_input()  # 获取用户输入的卡密

if len(user_input) < 32:  # 检查输入长度并验证卡密
    print("请输入正确卡密长度!")
else:
    if user_input in key():  # 检查输入长度并验证卡密
        print("验证成功!")
    else:
        print("验证失败,卡密不存在!")
        print("程序将于3秒后关闭")
        time.sleep(3)