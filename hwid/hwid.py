import subprocess

def get_hardware_id():
    # Windows系统获取硬件ID的示例命令
    # 请根据你的需求调整命令，这里以获取CPU序列号为例
    cmd = 'wmic cpu get ProcessorId'
    try:
        hwid = subprocess.check_output(cmd, shell=True).decode().split('\n')[1].strip()
        return hwid
    except Exception as e:
        print(f"无法获取硬件ID: {e}")
        return None

# 调用函数并打印其返回值
hwid = get_hardware_id()
if hwid:
    print(f"当前设备的硬件ID是: {hwid}")
else:
    print("无法获取硬件ID。")
