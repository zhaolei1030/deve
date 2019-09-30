import os
import paramiko
from datetime import datetime, timedelta, date
def connect():
    """
    连接远程ssh服务器
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('xx.xxx.xx.xxx',username='xxxxx',password='xxxxx',allow_agent=True)
        return ssh
    except:
        return None
def exec_commands(conn,cmd):
    """
    执行cmd命令
    :param conn:
    :param cmd:
    :return:
    """
    stdin,stdout,stderr = conn.exec_command(cmd)
    results=stdout.read()
    return results
def getDateTime(number):
    """
    转换过去时间
    :param number:
    :return:
    """
    oneday = timedelta(days=number)
    now = datetime.now()
    today = datetime(now.year, now.month, now.day) + oneday
    today = today.strftime('%Y%m%d')
    return today
ssh = connect()
dirs = exec_commands(ssh,'ls /data/all')
dirs=str(dirs,'utf-8')
dirs = dirs.split('\n')
print(type(dirs))

command = 'ls path'
r = os.popen(command)
info = os.lisdir('path')
download_list = []
with open('path/total_data.txt','r',encoding='utf-8')as f:
    for i in f:
        i = i.replace('\n','')
        download_list.append(i)

number = 0
for dir in dirs:
    if dir not in download_list:
        if number >= 80:
            break
        if dir != '':
            print(dir)
            number += 1
            os.system('scp -r username@xx.xx.xxx.xxx:path/{} path'.format(dir))
            with open('/path/total_data.txt', 'a', encoding='utf-8')as total_data:
                total_data.write(dir)
                total_data.write('\n')
            with open('path/{}.txt'.format(getDateTime(0)), 'w', encoding='utf-8')as f2:
                f2.write(i)
                f2.write('\n')
    else:
        # print('{} have existed'.format(dir))
        None
