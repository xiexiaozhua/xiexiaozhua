import json
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, Toplevel, Label, Entry, Button, Checkbutton, BooleanVar, messagebox
import subprocess
import openai
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import hashlib
import time

print("恭喜你发现了彩蛋!")
print("api密钥为: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")

def key_user_input():
    key_user_input = input("请输入你的卡密:")
    return key_user_input

def key():
    key = requests.get("https://github.com/xiexiaozhua/xiexiaozhua/blob/main/key.html").text
    return key

user_input = key_user_input()  # 获取用户输入的卡密


def get_hwid():
    FLAG = 0x08000000
    cpu_info = subprocess.check_output('wmic cpu get ProcessorId', shell=True, creationflags=FLAG).decode().split('\n')[
        1].strip()
    disk_info = \
    subprocess.check_output('wmic diskdrive get SerialNumber', shell=True, creationflags=FLAG).decode().split('\n')[
        1].strip()
    motherboard_info = \
    subprocess.check_output('wmic baseboard get SerialNumber', shell=True, creationflags=FLAG).decode().split('\n')[
        1].strip()
    hwid = hashlib.md5((cpu_info + disk_info + motherboard_info).encode()).hexdigest()
    return hwid


def user_hwid():
    user_hwid = requests.get("https://github.com/xiexiaozhua/xiexiaozhua/blob/main/index.html").text
    return user_hwid


# 尝试加载保存的设置
settings_file = 'settings.json'
try:
    with open(settings_file, 'r') as f:
        settings = json.load(f)
        # 确保所有期望的键都存在
        settings.setdefault("night_mode", False)
        settings.setdefault("user_name", "You")
        settings.setdefault("assistant_name", "GPT-3.5")
        settings.setdefault("api_keys", [])
        settings.setdefault("save_api_keys", False)
        settings.setdefault("current_key_index", 0)
        settings.setdefault("window_title", "GPT-3.5 Chat")
except (FileNotFoundError, json.JSONDecodeError):
    # 如果文件不存在或解码失败，提供一套默认设置
    settings = {
        "night_mode": False,
        "user_name": "You",
        "assistant_name": "GPT-3.5",
        "api_keys": [],
        "save_api_keys": False,
        "current_key_index": 0,
        "window_title": "GPT-3.5 Chat"
    }
    with open(settings_file, 'w') as f:
        json.dump(settings, f)  # 创建默认的设置文件
window_title = settings.get("window_title", "GPT-3.5 Chat")  # 如果找不到设置，使用默认值

# 在尝试加载设置的代码块后添加
if "window_title" not in settings:
    settings["window_title"] = "GPT-3.5 Chat"  # 默认窗口标题

def apply_settings():
    if settings["night_mode"]:
        chat_history.config(bg="black", fg="white")
        entry.config(bg="gray", fg="white")
        window.config(bg="gray")
    else:
        chat_history.config(bg="white", fg="black")
        entry.config(bg="white", fg="black")
        window.config(bg="white")
    window.title(settings["window_title"])  # 应用窗口标题设置


def switch_api_key():
    global current_key_index
    current_key_index = (settings["current_key_index"] + 1) % len(settings["api_keys"])
    settings["current_key_index"] = current_key_index
    openai.api_key = settings["api_keys"][current_key_index]

def chat_with_gpt(prompt, callback):
    """
    异步与GPT-3交互并通过回调函数返回结果。
    """
    def inner_chat():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            message = response.choices[0].message['content']
        except Exception as e:
            message = str(e)
        callback(message)  # 使用回调函数返回消息

    # 使用线程异步调用API
    thread = threading.Thread(target=inner_chat)
    thread.start()

def on_send():
    user_input = entry.get().strip()
    if user_input:
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"{settings['user_name']}: " + user_input + "\n")
        chat_history.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

        def callback(message):
            append_response(chat_history, message, name=settings['assistant_name'])

        chat_with_gpt(user_input, callback)

def get_api_key_from_user(force_prompt=False):
    if not settings["api_keys"] or force_prompt:
        api_key_window = Toplevel(window)
        api_key_window.title("密钥")

        Label(api_key_window, text="api密钥:").grid(row=0, column=0)
        api_key_entry = Entry(api_key_window)
        api_key_entry.grid(row=0, column=1)

        save_api_keys_var = BooleanVar(value=settings["save_api_keys"])
        Checkbutton(api_key_window, text="保存api密钥", variable=save_api_keys_var).grid(row=1, columnspan=2)

        def save_api_key():
            api_key = api_key_entry.get()
            if api_key:
                settings["api_keys"] = [api_key]
                settings["save_api_keys"] = save_api_keys_var.get()
                settings["current_key_index"] = 0
                if settings["save_api_keys"]:
                    with open(settings_file, 'w') as f:
                        json.dump(settings, f)
                openai.api_key = api_key
                api_key_window.destroy()
            else:
                messagebox.showerror("错误", "不要输入空值!")

        Button(api_key_window, text="保存", command=save_api_key).grid(row=2, columnspan=2)
    elif settings["api_keys"]:
        openai.api_key = settings["api_keys"][settings["current_key_index"]]

def open_settings():
    settings_window = Toplevel(window)
    settings_window.title("设置")

    Label(settings_window, text="用户名:").grid(row=0, column=0)
    user_name_entry = Entry(settings_window)
    user_name_entry.insert(0, settings["user_name"])
    user_name_entry.grid(row=0, column=1)

    Label(settings_window, text="对方回复你的名字:").grid(row=1, column=0)
    assistant_name_entry = Entry(settings_window)
    assistant_name_entry.insert(0, settings["assistant_name"])
    assistant_name_entry.grid(row=1, column=1)

    night_mode_var = BooleanVar(value=settings["night_mode"])
    night_mode_check = Checkbutton(settings_window, text="夜间模式(貌似有bug)", variable=night_mode_var)
    night_mode_check.grid(row=2, columnspan=2)

    Label(settings_window, text="窗口标题:").grid(row=3, column=0)
    window_title_entry = Entry(settings_window)
    window_title_entry.insert(0, settings.get("window_title", "GPT-3.5 Chat"))  # 使用get确保向后兼容性
    window_title_entry.grid(row=3, column=1)

    Button(settings_window, text="更新api密钥", command=lambda: get_api_key_from_user(force_prompt=True)).grid(row=4, columnspan=2)

    def save_settings():
        settings["user_name"] = user_name_entry.get()
        settings["assistant_name"] = assistant_name_entry.get()
        settings["night_mode"] = night_mode_var.get()
        settings["window_title"] = window_title_entry.get()  # 保存窗口标题设置
        apply_settings()
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
        settings_window.destroy()
    save_button = Button(settings_window, text="保存", command=save_settings)
    save_button.grid(row=6, columnspan=2)  # 确保Save按钮在最后一行
    save_titel = Button(settings_window, text="刷新标题", command=update_ui_elements())
    save_titel.grid(row=5, columnspan=2)  # 确保Save按钮在最后一行




    def save_settings():
        settings["user_name"] = user_name_entry.get()
        settings["assistant_name"] = assistant_name_entry.get()
        settings["night_mode"] = night_mode_var.get()
        settings["window_title"] = window_title_entry.get()  # 保存窗口标题设置
        apply_settings()
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
        settings_window.destroy()
        save_button = Button(settings_window, text="保存", command=save_settings)
        save_button.grid(row=5, columnspan=2)


def update_ui_elements():
    window_title = settings.get("window_title", "GPT-3.5 Chat")
    window.title(window_title)
def append_response(widget, message, name="", delay=50):
    def display_next_char(message, index=0):
        if index < len(message):
            widget.config(state=tk.NORMAL)
            if index == 0 and name:  # 如果是新消息（非用户输入），先添加发送者的名称
                widget.insert(tk.END, f"{name}: ")
            widget.insert(tk.END, message[index])
            widget.config(state=tk.DISABLED)
            widget.yview(tk.END)
            # 计划显示下一个字符
            widget.after(delay, lambda: display_next_char(message, index + 1))
        elif name:  # 如果是新消息（非用户输入），在消息后添加换行
            widget.after(delay, lambda: append_response(widget, "\n", delay=delay))

    display_next_char(message)

def apply_settings():
    if settings["night_mode"]:
        chat_history.config(bg="black", fg="white")
        entry.config(bg="gray", fg="white")
        window.config(bg="gray")
    else:
        chat_history.config(bg="white", fg="black")
        entry.config(bg="white", fg="black")
        window.config(bg="white")


if len(user_input) < 32:  # 检查输入长度并验证卡密
    messagebox.showerror("错误","卡密长度错误！")
else:
    if user_input in key():  # 检查输入长度并验证卡密
        messagebox.showinfo("验证成功!","欢迎使用 ")
        messagebox.showinfo("验证成功!","如果没有绑定HWID,请绑定HWID")
        if get_hwid() in user_hwid():
            window = tk.Tk()
            window.title(window_title)
            night_mode = settings.get('night_mode')
            frame = tk.Frame(window)
            scrollbar = tk.Scrollbar(frame)
            chat_history = scrolledtext.ScrolledText(frame, state='disabled', width=70, height=20)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            frame.pack()

            entry = tk.Entry(window, width=70)
            entry.bind("<Return>", lambda event: on_send())
            entry.pack(pady=10)

            send_button = tk.Button(window, text="发送", command=on_send)
            send_button.pack()

            settings_button = tk.Button(window, text="设置", command=open_settings)
            settings_button.pack()

            apply_settings  # 应用默认设置或已保存的设置
            get_api_key_from_user()  # 在程序启动时尝试加载API密钥
            window.mainloop()

        else:
            messagebox.showerror("错误", "HWID不匹配，请绑定HWID。")
            messagebox.showinfo("你的HWID", f"当前的HWID是:{get_hwid()} ")
            messagebox.showinfo("", "需要复制请到控制台")
            print(f"当前的HWID是:{get_hwid()} ")
            print("程序将于10秒后关闭")
            print("10")
            time.sleep(1)
            print("9")
            time.sleep(1)
            print("8")
            time.sleep(1)
            print("7")
            time.sleep(1)
            print("6")
            time.sleep(1)
            print("5")
            time.sleep(1)
            print("4")
            time.sleep(1)
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("END")
            time.sleep(0.5)
    else:
        messagebox.showerror("验证失败","请输入正确卡密！")
        messagebox.showinfo("程序即将关闭", "1秒后关闭程序")
        time.sleep(1)