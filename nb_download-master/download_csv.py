import pandas as pd
import _thread
import os
import paramiko

download_list = []
with open('path/total_data.txt','r',encoding='utf-8')as f:
    for i in f:
        i = i.replace('\n','')
        download_list.append(i)
with open('all.csv','r')as info:
    count = 0
    url_list = []
    for pic_data in info:
        pic_data = pic_data.replace("'",'')
        pic_data = pic_data.split(',')
        if pic_data[0] not in download_list:
            if not os.path.exists('path/{}'.format(pic_data[0])):
                count += 1
                if count > 1:
                    print('end')
                    break
                os.system('mkdir path/{}'.format(pic_data[0]))
                with open('path/total_data.txt', 'a', encoding='utf-8')as total_data:
                    total_data.write(pic_data[0])
                    total_data.write('\n')
            os.system('wget -P path/{} {}'.format(pic_data[0], pic_data[2]))
