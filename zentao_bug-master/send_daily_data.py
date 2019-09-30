import matplotlib.pyplot as plt
import matplotlib as mpl
from ftplib import FTP
import pandas as pd
import requests
import json
from datetime import datetime
import time
from matplotlib.font_manager import FontProperties
import os
font = FontProperties(fname='font_path/opentype/noto/NotoSansCJK-Medium.ttc', size=14)
today_time = time.strftime(r'%Y-%m-%d', time.localtime(time.time()))
def ftpconnect(host, username, password):
    """
    连接ftp
    :param host:
    :param username:
    :param password:
    :return:
    """
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp
def uploadfile(ftp, remotepath, localpath):
    """
    上传文件到ftp
    :param ftp:
    :param remotepath:
    :param localpath:
    :return:
    """
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
data = []
mpl.rcParams['font.sans-serif']=['SimHei'] #指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
# 每日bug数量通知机器人_赵磊写
url = 'http://cd_url.com'
account = 'xxxxxx'
password = 'xxxxxx'
pro_dict = {'id': ['job_name', 'top_word', "token", 'job'],
            }

for pro_num1 in pro_dict:
    # pro_num1 = '114'
    session = requests.session()
    path = '/pro/user-login.html'
    session.post(url=url + path, data={"account": account, "password": password})
    path = '/pro/index.html'
    session.post(url=url + path, data={"account": account, "password": password})
    path = 'json_url.json'.format(pro_num1)
    content = session.get(url=url + path)
    content = content.text
    content = json.loads(content)
    content = json.loads(content['data'])
    # print(content)
    # 找到所有的项目版本
    version = []
    ori_version = []
    new_version = []
    for i in content['projects']:
        temp = content['projects'][i].replace(' ','')
        temp = temp.lower()
        if temp.startswith(pro_dict[pro_num1][1]):
            # print(temp)
            ori_version.append(content['projects'][i])
            new_version.append(content['projects'][i].lower().replace(' ',''))
            # print(i)
            mark_num.append(int(new_project[content['projects'][i]]))
    assist_list = sorted(mark_num,reverse= True)
    print(mark_num)
    print(assist_list)
    for i in assist_list:
        version.append(ori_version[mark_num.index(i)])
    # version.sort(reverse=True)
    new_project = {}


    for k,v in sorted(content['projects'].items()):
        new_project[v] = k
    # 初始化统计变量
    generation = -1
    cur_total = 0
    new_open, new_open_important, new_open_block, new_open_common, new_open_suggest = 0, 0, 0, 0, 0
    resolved, resolved_important, resolved_block, resolved_common, resolved_suggest = 0, 0, 0, 0, 0
    active, active_important, active_block, active_common, active_suggest = 0, 0, 0, 0, 0
    closed, closed_important, closed_block, closed_common, closed_suggest = 0, 0, 0, 0, 0
    now = datetime.now()
    compared_time = now.strftime('%Y-%m-%d')+' 18:00:00'

    # print(content['bugs'])
    while cur_total == 0:
        generation += 1
        pro_num = new_project[version[generation]]
        total = 0
        for i in content['bugs']:
            total += 1

            if i['project'] == pro_num:
                cur_total += 1
                severity = i["severity"]
                # print(i["severity"])
                op = datetime.strptime(i["openedDate"], "%Y-%m-%d %H:%M:%S")
                op = op.strftime('%Y-%m-%d')
                # 判断过去24h新开数量
                diff = datetime.strptime(compared_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(i['openedDate'], '%Y-%m-%d %H:%M:%S')
                if diff.days == 0:
                    if severity == "2":
                        new_open_important += 1
                    elif severity == "1" or severity == "5":
                        new_open_block += 1
                    elif severity == "3":
                        new_open_common += 1
                    elif severity == "4":
                        new_open_suggest += 1
                    new_open += 1
                # 判断当前版本关闭数量
                if i['status'] == "closed":
                    if severity == "2":
                        closed_important += 1
                    elif severity == "1" or severity == "5":
                        closed_block += 1
                    elif severity == "3":
                        closed_common += 1
                    elif severity == "4":
                        closed_suggest += 1
                    closed += 1
                # 判断当前版本激活数量
                if i['status'] == 'active':
                    if severity == "2":
                        active_important += 1
                    elif severity == "1" or severity == "5":
                        active_block += 1
                    elif severity == "3":
                        active_common += 1
                    elif severity == "4":
                        active_suggest += 1
                    active += 1
                # 判断当前版本已解决数量
                if i['status'] == 'resolved':
                    if severity == "2":
                        resolved_important += 1
                    elif severity == "1" or severity == "5":
                        resolved_block += 1
                    elif severity == "3":
                        resolved_common += 1
                    elif severity == "4":
                        resolved_suggest += 1
                    resolved += 1
        data = [[now.strftime('%m-%d'), new_open, resolved, active, closed]]
        index = ['date','new_open', 'today_slove', 'today_active', 'today_close']

    dt = pd.DataFrame(data, columns=index)
    data_saver = 'path/{}_data_{}.csv'.format(pro_dict[pro_num1][0],version[generation])
    print(data_saver)
    if not os.path.exists(data_saver):
        print('build new file')
        dt.to_csv(data_saver, header = True,mode= 'a', encoding='gb2312')
    else:
        dt.to_csv(data_saver, header = False,mode= 'a', encoding='gb2312')
    data = pd.read_csv(data_saver, encoding='gb2312')

#设置画布
    size = len(data['new_open'])/2
    if size <8:
        size = 8
    plt.figure(figsize=(size,size),dpi=80)
    plt.plot(data['date'], data['today_close'],label="today_close", linewidth=4, color = 'blue')
    plt.plot(data['date'], data['today_slove'],label = 'today_slove', linewidth=4, color = 'red')
    plt.plot(data['date'], data['today_active'],label = 'today_active', linewidth=4, color = 'green')
    plt.plot(data['date'], data['new_open'],label = 'new_open', linewidth=4, color = 'black')
# plt.title('line chart')
    plt.title('{}'.format(pro_dict[pro_num1][0]),size=20,fontproperties=font)
    plt.plot(size, max(data['today_slove']))
    plt.xlabel('time',size=15,fontproperties=font)
    plt.ylabel('number', size=15,fontproperties=font)
    plt.legend(prop = font)
    plt.savefig('/picture_url/{}{}.png'.format(pro_dict[pro_num1][3],today_time))
    plt.show()
    ftp = ftpconnect('xx.xx.xxx.x', 'xx', 'xxxxxx')
    uploadfile(ftp, '/bug_pic/{}{}.png'.format(pro_dict[pro_num1][3],today_time), 'picture_path/{}{}.png'.format(pro_dict[pro_num1][3],today_time))
    time.sleep(3)
    pic_url = 'http://xxx.xxx.xxx.x/bug_pic/{}{}.png'.format(pro_dict[pro_num1][3],today_time)
    # print(pic_url)
    text = "{}statictic report（until 18:00）  \n" \
"**total bugs**：{}  \n" \
"**current version**：{}  \n" \
"**current version total bugs**：{}  \n" \
"**today_close**：{}  \n" \
"- harm：{}  \n" \
"- important：{}  \n" \
"- normal：{}  \n" \
"***\n" \
"**today_slove**：{}  \n" \
"- harm：{}  \n" \
"- important：{}  \n" \
"- normal：{}  \n" \
"***\n" \
"**today_active**：{}  \n" \
"- harm：{}  \n" \
"- important：{}  \n" \
"- normal：{}  \n" \
"***\n" \
"**new_open**：{}  \n" \
"- harm：{}  \n" \
"- important：{}  \n" \
"- normal：{}  \n" \
"***\n" \
"![asr]({})".format(pro_dict[pro_num1][0], total, version[generation], cur_total, new_open, new_open_block,
           new_open_important,
           new_open_common, active, active_block, active_important, active_common,
           resolved, resolved_block, resolved_important, resolved_common,
           closed, closed_block, closed_important, closed_common,pic_url)
    print(text)
    def dingding(access_token, title, text, atMobiles, msg_type='markdown', isAtAll=False):

        url = "https://oapi.dingtalk.com/robot/send?access_token=" + access_token
        if msg_type == 'markdown':
            data = {
                "msgtype": msg_type,
                "at": {
                    "atMobiles": atMobiles,
                    "isAtAll": isAtAll
                },
                "media_id": text
            }
            return requests.post(url, json=data)

        title = "daily_report"
        dingding(access_token=pro_dict[pro_num1][2], title=title,
                 text=text, atMobiles=True, msg_type='markdown', isAtAll=False)