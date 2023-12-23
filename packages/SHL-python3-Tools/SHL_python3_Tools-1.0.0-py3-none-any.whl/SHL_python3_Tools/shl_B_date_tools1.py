import datetime





'''
#获取完整时间
'''
def get_FullDate():
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")#"年-月-日 时:分:秒"
    return time_str
        
        


def getAppoint():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    print(year, month, day, hour, minute, second)



'''
## 设置过期时间(时间戳)
fenZong = 60分钟
'''
def get_guoQiShiJian(fenZong):
        
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=fenZong) #可以计算
    return expiration_time


#时间戳 -> 日期时间
def shiJianChuo_convert_dateTime_oob(shiJianChuo):
    dttm = datetime.datetime.fromtimestamp( shiJianChuo)  # 时间戳转换为 datetime 对象
    return dttm


#获取时间戳
def get_shiJianChuo():
    return datetime.datetime.utcnow()