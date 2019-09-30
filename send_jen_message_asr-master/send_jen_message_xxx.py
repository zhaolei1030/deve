# coding: UTF-8
from bs4 import BeautifulSoup
import json as js
import requests
import sys
import io
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
project = 'pro_name'
job = 'job_name'
# num  = os.environ['ID']
num = sys.argv[1]
path = u'path/report.html'
# path = 'D:\May\\auto_send_rbinfo\\report.html'
with io.open(path, 'r', encoding='utf-8')as html:
    Soup = BeautifulSoup(html.read(), 'lxml')
    scripts = Soup.find_all('script')
    print('this is length of scripts')
    # print(len(scripts))
    for script in scripts:
        if 'window.output["stats"]' in script.string:
            target = script.string[26:-2]
            target = target.split(']')
            for tar in target:
                for items in tar.split('['):
                    if items == '':
                        continue
                    elif items == ',':
                        continue
                    else:
                        print(items)
                        items = items.replace(',"','。')
                        items = items.replace(',', '/')
                        items = items.replace('。', ',"')
                        items = items.split('/')
                        for item in items:
                            dicts = js.loads(item)
                            if dicts['label'] == 'All Tests':
                                # print(dicts)
                                paased = int(dicts['pass'])
                                failed = int(dicts['fail'])
                                total = paased + failed
                                print(total)
                                print(paased)
                                pass_per = round(float(paased)/total,4)*100
                                duration = dicts['elapsed']
                                job_url = 'http://url/{}/robot '.format(num)
text = """test result report  
**project**：{}  
**job**：{}  
**total number**：{}  
**pass rate**：{}%  
**pass number**：{}  
**fail number**：{}  
**run time**：{}  
**Job URL**：{}  
""".format(project,job, total, pass_per, paased, failed, duration, job_url)
# print(text)
token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'



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
    title = "test report"
    dingding(access_token=token, title=title, text=text, atMobiles=True,  msg_type='markdown', isAtAll=False)