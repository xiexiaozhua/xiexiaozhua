import os

def save_settings():
    # 获取当前工作目录作为根路径
    root_path = os.getcwd()

    # 定义文件路径
    file_path = os.path.join(root_path, 'Setting.txt')

    # 获取用户输入
    lujin = input("请输入路径：")
    zhanghao = input("请输入账号：")
    mima = input("请输入密码：")

    # 将用户输入的数据写入文件
    with open(file_path, 'w') as settings_file:
        settings_file.write(f'lujin={lujin}\n')
        settings_file.write(f'zhanghao={zhanghao}\n')
        settings_file.write(f'mima={mima}\n')

# 调用函数保存设置
save_settings()