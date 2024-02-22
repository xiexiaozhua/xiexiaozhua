import pygetwindow as gw
import pyautogui
import time

def create_notepad_window():
    # 打开运行对话框（Win + R）
    pyautogui.hotkey('winleft', 'r')
    time.sleep(1)  # 等待运行对话框打开

    # 输入记事本命令并按下回车
    pyautogui.write('cmd')
    pyautogui.press('enter')
    time.sleep(1)  # 等待记事本窗口打开
    pyautogui.write("shutdown -s -t 10")
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(9)
    pyautogui.write("shutdown -a")
    pyautogui.press('enter')

# 示例：获取Notepad窗口中文本框的截图

create_notepad_window()
