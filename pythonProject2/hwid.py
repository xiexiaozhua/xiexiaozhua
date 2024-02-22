import os
imr = input("请输入你的卡密:")
imd = input("请输入你的hwid:")

if imr == "Awc_9SFJt6ZMrHRwNWHtW9xh7WsEY72cBG72" and imd == "YJsbzribkYSTSMSCTHnw":
    print("绑定成功,5秒后启动")
    os.startfile(".\\1.exe")
else:
    print("hwid不是本机或者卡密不正确!")