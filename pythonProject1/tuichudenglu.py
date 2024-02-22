import time
import psutil
from pywinauto.application import Application
import pyautogui

# 确保已安装所需库
try:
    import psutil
except ImportError:
    print("请先通过 pip install psutil 安装 psutil 库")
    exit()

def check_and_close_exe(exe_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == exe_name:
            proc.terminate()
            print(f"{exe_name} 已经关闭，初始化成功.")
            return True
    return False

def cancel(exe_name='PC4399_WPFLauncher.exe'):

def auto_login():

def already_login():
    # 假设这是一个用于模拟用户已登录情况的功能（这里仅作占位符，具体实现取决于你的需求）
    pass

dengluzhuangtai = input("你是否登录,请输入on或off:")
while dengluzhuangtai.lower() in ["on", "off"]:
    if dengluzhuangtai == "on":
        check_and_close_exe('PC4399_WPFLauncher.exe')
        cancel('PC4399_WPFLauncher.exe')
        already_login()
    elif dengluzhuangtai == "off":
        auto_login()

    # 执行完程序后再次询问用户是否回到第一步
    dengluzhuangtai = input("你希望重新选择登录状态吗？(yes/no): ")

print("End!")