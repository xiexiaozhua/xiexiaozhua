import os


def read_settings():
    # 获取当前工作目录作为根路径
    root_path = os.getcwd()
    # 定义文件路径
    file_path = os.path.join(root_path, 'Setting.txt')

    # 获取用户输入
    lujin = input("请输入路径：")
    zhanghao = input("请输入账号：")
    mima = input("请输入密码：")


    # 检查文件是否存在
    if os.path.exists(file_path):
        # 打开文件以读取模式 ('r')
        with open(file_path, 'r') as settings_file:
            lines = settings_file.readlines()

            # 解析每行内容并创建一个字典存储键值对
            settings_dict = {}
            for line in lines:
                key, value = line.strip().split('=', 1)
                settings_dict[key] = value

            # 将读取到的设置赋值给全局变量
            try:
                lujin = settings_dict['lujin']
                zhanghao = settings_dict['zhanghao']
                mima = settings_dict['mima']

                print("读取到的设置如下：")
                print(f"lujin: {lujin}")
                print(f"zhanghao: {zhanghao}")
                print(f"mima: {mima} ")

            except KeyError as e:
                print(f"无法找到键 '{e.args[0]}'，请确保文件中有完整的键值对。")
    else:
        print(f"文件'{file_path}'不存在，无法读取数据。")


# 调用函数读取设置并将它们赋值给全局变量
read_settings()

# 现在可以在函数外部访问这些变量
print(f"lujin={lujin}, zhanghao={zhanghao}")