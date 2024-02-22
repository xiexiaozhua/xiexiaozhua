import time
import os
iop = input("请输入你的卡密:")

if iop == "Awc_zrBynB2bXhJJsYfaKMca9EikmP9Jnsk5":
     print("恭喜验证成功!请绑定你的hwid")
     print("你的HWID为:ZdTeePRwbAejQayNGrHE")
     imd = input("请输入你的hwid:")
     if  imd == "ZdTeePRwbAejQayNGrHE":
          print("绑定成功,5秒后启动")
          os.startfile(".\\1.exe")
          print("启动成功!")
     else:
          print("hwid不是本机或者卡密不正确!")
else:
     print("卡密验证失败!请输入正确卡密")
     print("程序将于5秒后关闭...")
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
     print("0")