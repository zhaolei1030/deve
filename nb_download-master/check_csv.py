import pandas as pd
import os
import paramiko

download_list = []
with open('path/total_data.txt','r',encoding='utf-8')as f:
    for i in f:
        i = i.replace('\n','')
        download_list.append(i)

url_dict = {}
with open('path/file.csv','r')as info:     #将所有问题集存入内存，按照问题划分为不同字典，键为问题，值为url链接
    for pic_data in info:
        pic_data = pic_data.replace("'",'')
        pic_data = pic_data.split(',')
        if pic_data[0] not in url_dict:
            url_dict[pic_data[0]] = [pic_data[2]]
        else:
            url_dict[pic_data[0]].append(pic_data[2])
        url_dict[pic_data[0]].append(pic_data[0])
count = 0
print ('start download')
for question in url_dict:         #判断问题是否下载过并下载
    if question not in download_list:
        count += 1
        if not os.path.exists('path/{}'.format(question)):
            os.system('mkdir path/{}'.format(question))
            for pic in url_dict[question]:
                os.system('wget -P path/{} {}'.format(question, pic))
        if count >= 2:
            break
    else:
        print('have existed')