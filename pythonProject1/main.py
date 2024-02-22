import time
import psutil
from pywinauto.application import Application
import pyautogui
import keyboard
import sys
import os

por = "woshishabi"  # 将"=="改为 "=", 这里应该是赋值而非比较
app_path = r'C:\\Program Files (x86)\\Netease\\PC4399_MCLauncher\\PC4399_WPFLauncher.exe'

def auto_login():
    if not check_and_close_exe('steam.exe'):
        print("PC4399_WPFLauncher.exe 未运行，开始启动程序...")

    try:
        app = Application().start(cmd_line=app_path)

        # 等待程序窗口加载
        time.sleep(3)  # 这里的等待时间可能需要根据实际情况调整

        # 获取主窗口并最大化
        main_window = app.window(title='steam')
        main_window.maximize()  # 添加这一行以最大化窗口

    except Exception as e:
        print(f"启动或操作窗口时出错: {e}")

def check_and_close_exe(exe_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == exe_name:
            proc.terminate()
            print(f"{exe_name} 已经关闭，初始化成功.")
            return True
    return False

# 将条件判断放在主程序块中
if por == "woshishabi":
    auto_login()