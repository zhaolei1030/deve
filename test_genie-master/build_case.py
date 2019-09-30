#-- coding:UTF-8 --
from bs4 import BeautifulSoup
import math
import requests
import jenkins
import sys
import time
import io
import os
import itertools
import json
from xpinyin import Pinyin
# reload(sys)
# sys.setdefaultencoding( "utf-8" )
session = requests.session()
path = 'https://wiki_url'
session.post(url= path, data={"os_username": 'XXXXX', "os_password": 'XXXXX'})
url="https://wiki_url"
url = sys.argv[1]
tx = session.get(url=url)
tx.encoding=tx.apparent_encoding
tx = tx.text
# print(tx)
soup=BeautifulSoup(tx,"html.parser")
all_table = soup.find_all('table')
table_dict = {}
table_number = 0
# print(len(all_table))
def com_case(tar_list):
    """
    对case进行排列组合
    :param tar_list:
    :return:
    """
    total_combination = []
    for num in range(1,len(tar_list)+1):
        tmp_list = itertools.combinations(tar_list, num)
        for one in tmp_list:
            total_combination.append(one)
    return total_combination

table = all_table[0]
table_dict[table_number] = []
case_list = []
all_tr = table.find_all('tr')
    # print(all_tr)
num = 0
start_repeat = 0
# print(all_tr)
for tr in all_tr:
    table_dict[table_number].append([])
    for td in tr:
        # print(td)
        temp = [str(x.string) for x in td]
        temp = ''.join(temp)
        table_dict[table_number][num].append(temp)         #save table information to list
    num += 1
table = table_dict[0]
if not os.path.exists('/path'):
    os.system('mkdir /path')
with io.open('/path/case.robot', 'w', encoding='utf-8')as f:
# print(table)
# with open('D:/May/auto_build/case.robot', 'w')as f:
    f.write('*** Settings ***\nLibrary          requests\nLibrary          json\nLibrary          Collections\nLibrary          RequestsLibrary\nLibrary          urllib3\n\n*** Variables ***\n')
    for item_num in range(len((table[1]))):
        # print(table[1][item_num])
        if table[1][item_num] != 'None':
            f.write('${%s}        %s\n'%(table[0][item_num],table[1][item_num]))
    f.write('\n*** Test Cases ***\n')
for table in all_table[-1] :
    table_dict[table_number] = []
    case_list = []
    all_tr = table.find_all('tr')
        # print(all_tr)
    num = 0
    start_repeat = 0
    if len(all_tr) == 0:
        continue
    # print(all_tr)
    for tr in all_tr:
        table_dict[table_number].append([])
        for td in tr:
            # print(td)
            temp = td.get_text()
            table_dict[table_number][num].append(temp)         #save table information to list
        num += 1
    table = table_dict[0]
    for case_num in range(len(table)-1):
        with io.open('/path/case.robot', 'a', encoding='utf-8')as f:
            f.write(table[case_num+1][1]+'\n')
            if table[case_num + 1][2] == '1':
                f.write('    Disable Warnings\n')
            if table[case_num + 1][3] != '0':
                f.write('    ${headers}    create dictionary    %s\n'%table[case_num + 1][3])
                f.write('    Create Session    myapi    ${URL}    headers=${headers}\n')
            else:
                f.write('    Create Session    myapi    ${URL}\n')
            if table[case_num + 1][4] != '0':
                f.write('    @{%s}    create list    ${%s}\n'%(table[case_num + 1][4],table[case_num + 1][4]))
            if table[case_num+1][5] != '0':
                information = table[case_num+1][5].replace('\n','')
                # print(information)
                information = information.replace('；', ';')
                f.write('    ${info}=    Create dictionary')
                if ';' in information:
                    information = information.split(';')
                    for info_num in range(len(information)):
                        f.write('    %s'%information[info_num])
                    f.write('\n')
                else:
                    f.write('    %s\n'%information)
            if table[case_num+1][6] != '0':
                resp = table[case_num+1][6].replace('\n','')
                resp = resp.replace('；', ';')
                resp = resp.split(';')
                if (table[case_num+1][5] != '0') and (table[case_num+1][3] != '0'):
                    f.write('    ${resp}=    %s request    myapi    %s    headers=${headers}    data=${info}\n'%(resp[0],resp[2]))
                elif (table[case_num + 1][5] == '0') and (table[case_num + 1][3] != '0'):
                    f.write('    ${resp}=    %s request    myapi    %s    headers=${headers}\n' % (resp[0], resp[2]))
                else:
                    f.write('    ${resp}=    %s request    myapi    %s\n' % (resp[0], resp[2]))
                if resp[1] == 'log':
                    f.write('    log    ${resp.content}\n')
                # print(table[case_num+1][4])
            if table[case_num + 1][7] != '0':
                f.write('    Should Be Equal As Strings    ${resp.status_code}    %s\n'%table[case_num + 1][7])
            if table[case_num + 1][8] != '0':
                resp = table[case_num+1][8].replace('\n','')
                resp = resp.replace('；', ';')
                resp = resp.split(';')
                f.write('    ${resp}    %s    ${resp.%s}\n'%(resp[0],resp[1]))
            if table[case_num + 1][9] != '0':
                suite = table[case_num + 1][9].replace('；',';')
                suite = suite.split(';')
                f.write('    set suite variable    ${%s}    ${%s}\n'%(suite[0],suite[1]))
            if table[case_num + 1][10] != '0':
                suite = table[case_num + 1][10].replace('；',';')
                suite = suite.split(';')
                f.write('    set suite variable    ${%s}    ${%s}\n'%(suite[0],suite[1]))
            f.write('\n')

ori_url = 'http://jenkins_url'
server = jenkins.Jenkins(ori_url, username="xxxxx", password="xxxxx")
jobs = server.get_all_jobs()
new_job_name = 'job_name'+time.strftime(r'%Y-%m-%d-%H-%M', time.localtime(time.time()))
# print(server.get_job_config("automation_notify"))
print(new_job_name)
server.copy_job('Axer_AutomationTemplate', new_job_name)
server.disable_job(new_job_name)
command = 'scp -P xxxxx -r /dic_path root@xxx.xxx.xx.xxx:/file_path'
print(command)
os.system(command)
# # p=os.popen(command)
server.enable_job(new_job_name)
command = 'scp -P xxxxx -r /dic_path root@xxx.xxx.xx.xxx:/file_path/{}'.format(new_job_name)
time.sleep(5)
p=os.system(command)
server.build_job(new_job_name,{'robot': 'job_name'})
# print(command)