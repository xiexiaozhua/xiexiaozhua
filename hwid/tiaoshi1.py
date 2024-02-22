import threading
import tkinter as tk
from tkinter import scrolledtext, Toplevel, Label, Entry, Button, Checkbutton, BooleanVar, messagebox
from threading import Thread
import openai
import json
import os

# 尝试加载保存的设置
settings_file = 'settings.json'
try:
    if os.path.exists(settings_file) and os.path.getsize(settings_file) > 0:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        raise FileNotFoundError
except (FileNotFoundError, json.JSONDecodeError):
    settings = {
        "night_mode": False,
        "user_name": "You",
        "assistant_name": "GPT-3.5",
        "api_keys": [],
        "save_api_keys": False,
        "current_key_index": 0
    }

def apply_settings():
    if settings["night_mode"]:
        chat_history.config(bg="black", fg="white")
        entry.config(bg="gray", fg="white")
        window.config(bg="gray")
    else:
        chat_history.config(bg="white", fg="black")
        entry.config(bg="white", fg="black")
        window.config(bg="white")

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
    user_input = entry.get()
    if user_input.strip() != '':
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"{settings['user_name']}: " + user_input + "\n")
        chat_history.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

        def append_response(message):
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"{settings['assistant_name']}: " + message + "\n")
            chat_history.config(state=tk.DISABLED)
            chat_history.yview(tk.END)

        chat_with_gpt(user_input, append_response)

def get_api_key_from_user(force_prompt=False):
    if not settings["api_keys"] or force_prompt:
        api_key_window = Toplevel(window)
        api_key_window.title("Enter OpenAI API Key")

        Label(api_key_window, text="API Key:").grid(row=0, column=0)
        api_key_entry = Entry(api_key_window)
        api_key_entry.grid(row=0, column=1)

        save_api_keys_var = BooleanVar(value=settings["save_api_keys"])
        Checkbutton(api_key_window, text="Save API Key", variable=save_api_keys_var).grid(row=1, columnspan=2)

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
                messagebox.showerror("Error", "API Key cannot be empty.")

        Button(api_key_window, text="Save", command=save_api_key).grid(row=2, columnspan=2)
    elif settings["api_keys"]:
        openai.api_key = settings["api_keys"][settings["current_key_index"]]

def open_settings():
    settings_window = Toplevel(window)
    settings_window.title("Settings")

    Label(settings_window, text="User Name:").grid(row=0, column=0)
    user_name_entry = Entry(settings_window)
    user_name_entry.insert(0, settings["user_name"])
    user_name_entry.grid(row=0, column=1)

    Label(settings_window, text="Assistant Name:").grid(row=1, column=0)
    assistant_name_entry = Entry(settings_window)
    assistant_name_entry.insert(0, settings["assistant_name"])
    assistant_name_entry.grid(row=1, column=1)

    night_mode_var = BooleanVar(value=settings["night_mode"])
    night_mode_check = Checkbutton(settings_window, text="Night Mode", variable=night_mode_var)
    night_mode_check.grid(row=2, columnspan=2)

    Button(settings_window, text="Update API Key", command=lambda: get_api_key_from_user(force_prompt=True)).grid(row=3, columnspan=2)

    def save_settings():
        settings["user_name"] = user_name_entry.get()
        settings["assistant_name"] = assistant_name_entry.get()
        settings["night_mode"] = night_mode_var.get()
        apply_settings()
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
        settings_window.destroy()

    save_button = Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=4, columnspan=2)


def append_response(widget, message, name="", delay=50):
    """
    逐字显示消息到聊天历史中。

    :param widget: 要更新的文本控件。
    :param message: 要显示的消息文本。
    :param name: 发送者的名称。
    :param delay: 每个字显示之间的延迟时间，单位为毫秒。
    """

    # 这是正确定义的append_response，确保它只定义一次，不要再函数内部重定义
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

    def on_send():
        user_input = entry.get().strip()
        if user_input:
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"{settings['user_name']}: " + user_input + "\n")
            chat_history.config(state=tk.DISABLED)
            entry.delete(0, tk.END)

            # 修改这里，使用回调正确地更新UI
            def callback(message):
                append_response(chat_history, message, name=settings['assistant_name'])

            chat_with_gpt(user_input, callback)


window = tk.Tk()
window.title("GPT-3.5 Chat")

frame = tk.Frame(window)
scrollbar = tk.Scrollbar(frame)
chat_history = scrolledtext.ScrolledText(frame, state='disabled', width=70, height=20)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame.pack()

entry = tk.Entry(window, width=70)
entry.bind("<Return>", lambda event: on_send())
entry.pack(pady=10)

send_button = tk.Button(window, text="Send", command=on_send)
send_button.pack()

settings_button = tk.Button(window, text="Settings", command=open_settings)
settings_button.pack()

apply_settings()  # 应用默认设置或已保存的设置
get_api_key_from_user()  # 在程序启动时尝试加载API密钥

window.mainloop()
