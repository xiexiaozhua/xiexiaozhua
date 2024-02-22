import subprocess

# 使用subprocess.run()执行命令并获取返回值（包括标准输出和标准错误）
# 这是一个基本的例子，假设要执行dir命令（Windows环境下）
result = subprocess.run(['dir'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# 获取命令的标准输出（stdout）和标准错误（stderr），并解码为字符串（默认是字节流）
stdout = result.stdout.decode()
stderr = result.stderr.decode()

# 打印标准输出
print("Standard Output:\n", stdout)

# 如果需要交互式地模拟输入，可以使用Popen创建一个进程，并向其stdin写入数据
with subprocess.Popen('your_command', stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
    # 写入模拟的输入
    p.stdin.write("your_input\n")
    p.stdin.flush()  # 确保输入被立即发送到子进程
    output = p.stdout.readline()  # 读取一行输出

# 输出结果
print("Command Output:\n", output.strip())