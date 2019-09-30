import requests
from datetime import datetime, timedelta, date
import time
import os
f = 'path/statistic_info.txt'
token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
total = []
with open(f, 'r',encoding='utf8') as f:
    for i in f:
        if i != '\n':
            s = i.split(':')
            total.append(s[1])
print(s)
valid_pic = int(total[0]) - int(total[1]) -int(total[2]) -int(total[3])
percent = (int(total[1]) +int(total[2]) +int(total[3]))*100/float(total[0])
ratio = str(round(float(percent),2))+'%'
def getDateTime(number):
    """
    转换过去时间
    :param number:
    :return:
    """
    oneday = timedelta(days=number)
    now = datetime.now()
    today = datetime(now.year, now.month, now.day) - oneday
    today = today.strftime('%Y%m%d')
    return today
time_stamp = getDateTime(0)
time_list = os.listdir('path')
print(time_list)
if time_stamp+'.txt' not in time_list:
    time_stamp = getDateTime(1)
text = """**result report**  
**total number**：{}  
**valid pic**：{}  
**clean rate**：{}  
**rotate number**：{}  
**dim number**：{}  
**no picture**：{}  
**result list**：path/{}.txt  
""".format(total[0],valid_pic,ratio,total[1],total[2],total[3],time_stamp)
print(text)


def dingding(access_token, title, text, atMobiles, msg_type='markdown', isAtAll=False):
    """
    发送钉钉消息
    :param access_token:
    :param title:
    :param text:
    :param atMobiles:
    :param msg_type:
    :param isAtAll:
    :return:
    """
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + access_token
    if msg_type == 'markdown':
        data = {
            "msgtype": msg_type,
            "at": {
                "atMobiles": atMobiles,
                "isAtAll": isAtAll
            },
            'markdown': {'title': title, 'text': text}
        }
        return requests.post(url, json=data)


if __name__ == '__main__':
    title = "data clean notification"
    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    t_t = time.mktime(today.timetuple())
    n_t = time.mktime(now.timetuple())
    print(t_t)
    print(t_t)
    print(int(n_t)-int(t_t))

    if (int(t_t) - int(n_t) > -28800) and (int(t_t) - int(n_t) < 0):
        print(1)
        time.sleep(int(n_t) - int(t_t))
    elif int(n_t) - int(t_t) < -75600:
        print(2)
        time.sleep(86400 - int(t_t) + int(n_t) + 28800)
    else:
        None
    dingding(access_token=to,  title=title,msg_type="markdown", atMobiles=[], isAtAll=True, text=text)