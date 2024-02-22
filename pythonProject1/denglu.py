import time
import psutil
from pywinauto.application import Application
import pyautogui
import keyboard
import sys
import os
dengluzhuangtai = input("你是否登录,请输入on or off(如果测试x，y坐标请输入:1),需要设置请输入2,必须先要设置才能使用!:")
lujin = None
zhanghao = None
mima = None
app_path = None
# 确保已安装所需库
def save_settings():
    root_path = os.getcwd()
    file_path = os.path.join(root_path, 'Setting.txt')

    # 获取用户输入
    lujin = input("请输入路径(必须是双斜杠)：")
    zhanghao = input("请输入账号：")
    mima = input("请输入密码：")
    x1 = input("你的账号框的右边的x轴,最好靠最右边又可以输入的地方:")
    y1 = input("你的账号框的右边的y轴,一定是4399账号!!!:")
    x2 = input("登录完账号的开始游戏的x轴:")
    y2 = input("登录完账号的开始游戏的y轴:")
    x3 = input("同意条款的x轴:")
    y3 = input("同意条款的y轴:")
    x4 = input("退出登录的x轴:")
    y4 = input("退出登录的y轴:")


    # 将用户输入的数据写入文件
    with open(file_path, 'w') as settings_file:
        settings_file.write(f'lujin={lujin}\n')
        settings_file.write(f'zhanghao={zhanghao}\n')
        settings_file.write(f'mima={mima}\n')
        settings_file.write(f'x1={x1}\n')
        settings_file.write(f'y1={y1}\n')
        settings_file.write(f'x2={x2}\n')
        settings_file.write(f'y2={y2}\n')
        settings_file.write(f'x3={x3}\n')
        settings_file.write(f'y3={y3}\n')
        settings_file.write(f'x4={x4}\n')
        settings_file.write(f'y4={y4}\n')
    app_path = lujin

def read_settings():
    # 获取当前工作目录作为根路径
    root_path = os.getcwd()
    file_path = os.path.join(root_path, 'Setting.txt')

    if os.path.exists(file_path):
        # 打开文件以读取模式 ('r')
        with open(file_path, 'r') as settings_file:
            lines = settings_file.readlines()

            # 解析每行内容并创建一个字典存储键值对
            settings_dict = {}
            for line in lines:
                key, value = line.strip().split('=', 1)
                settings_dict[key] = value

            try:
                app_path = settings_dict['lujin']  # 假设这里使用'路径'作为键
                lujin = settings_dict['lujin']
                zhanghao = settings_dict['zhanghao']
                mima = settings_dict['mima']
                x1 = int(settings_dict['x1'])  # 假设这里使用'路径'作为键
                y1 = int(settings_dict['y1'])
                x2 = int(settings_dict['x2'])
                y2 = int(settings_dict['y2'])
                x3 = int(settings_dict['x3'])
                y3 = int(settings_dict['y3'])
                x4 = int(settings_dict['x4'])
                y4 = int(settings_dict['y4'])



                return app_path, lujin, zhanghao, mima,x1,y1,x2,y2,x3,y3,x4,y4

            except KeyError as e:
                print(f"无法找到具体数值 '{e.args[0]}'，请确保文件中有完整的数值。")

# 调用函数读取设置并将它们赋值给全局变量

# 指定程序的完整路径

def check_and_close_exe(exe_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == exe_name:
            proc.terminate()
            print(f"{exe_name} 已经关闭，初始化成功.")
            return True
    return False

def cancel(exe_name='PC4399_WPFLauncher.exe'):
    # 检查并关闭已经存在的 PC4399_WPFLauncher.exe 进程
    if not check_and_close_exe(exe_name):
        print(f"{exe_name} 未运行，开始启动程序...")

    try:
        app = Application().start(cmd_line=app_path)

        # 等待程序窗口加载
        time.sleep(3)  # 这里的等待时间可能需要根据实际情况调整

        # 获取主窗口并最大化
        main_window = app.window(title='PC4399_WPFLauncher')  # 根据你的应用标题（通常是窗口标题而不是.exe文件名）替换

        if main_window.exists():
            main_window.maximize()
        pyautogui.click(x=x4, y=y4)

    except Exception as e:
        print(f"启动或操作窗口时出错: {e}")

def check_and_close_exe(exe_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == exe_name:
            proc.terminate()
            print(f"{exe_name} 已经关闭，初始化成功.")
            return True
    return False
def ceshi():
    pl = input("请输入多少秒检测一次:")
    number = float(pl)
    while True:
        if number < 0.2:
            print("很可能导致你的电脑变卡!")
            break
        # 获取鼠标当前位置
        x, y = pyautogui.position()

        # 输出到控制台
        print(f"当前鼠标位置: ({x}, {y})")

        # 为了防止控制台刷新过快，这里设置每秒更新一次
        time.sleep(number)


        if keyboard.is_pressed('p'):  # 检测 'p' 键是否被按下
                print("程序即将退出")
                sys.exit(0)

def auto_login():
    username = zhanghao
    password = mima



    if not check_and_close_exe('PC4399_WPFLauncher.exe'):
        print("PC4399_WPFLauncher.exe 未运行，开始启动程序...")

    try:
        app = Application().start(cmd_line=app_path)

        # 等待程序窗口加载
        time.sleep(3)  # 这里的等待时间可能需要根据实际情况调整

        # 获取主窗口并最大化
        main_window = app.window(title='PC4399_WPFLauncher')  # 根据你的应用标题（通常是窗口标题而不是.exe文件名）替换

        if main_window.exists():
            main_window.maximize()

        # 将鼠标移动到用户名输入框并点击（此处仅为示例，实际位置需根据你的程序窗口调整）
        pyautogui.click(x=x1, y=y1)
        for _ in range(3 * 10):  # 假设每秒可删除10个字符，根据实际速度调整
            pyautogui.press('backspace')
        pyautogui.write(username)
        pyautogui.press('tab')  # 跳转到密码输入框（如果程序是按TAB键切换的话）
        time.sleep(1)  # 等待输入框切换完成
        pyautogui.write(password)
        pyautogui.press('enter')  # 按下回车键进行登录
        time.sleep(1)
        pyautogui.click(x=x2, y=y2)
        time.sleep(1)
        pyautogui.click(x=x3,y=y3)

    except Exception as e:
        print(f"启动或操作窗口时出错: {e}")


if dengluzhuangtai == "on":
    read_settings()
    (app_path, lujin, zhanghao, mima,x1,x2,x3,y1,y2,y3,x4,y4) = read_settings()
    check_and_close_exe('steam.exe')
    cancel('steam.exe')


if dengluzhuangtai == "off":
    read_settings()
    (app_path, lujin, zhanghao, mima,x1,x2,x3,y1,y2,y3,x4,y4) = read_settings()
    auto_login()

if dengluzhuangtai == "1":
    ceshi()

if dengluzhuangtai == "2":
    read_settings()
    save_settings()

print("End!")
