#encoding:utf-8
import tarfile
import os
import json as js
from datetime import date
import time
from dateutil.rrule import rrule, DAILY
import sys
def untar(fname, dirs):
    t = tarfile.open(fname)
    t.extractall(path = dirs)
def utar_all(file_dir):
    """
    遍历文件夹下所有文件并解压
    :param file_dir:
    :return:
    """
    writeen_mark = 0
    for root,dirs,files in os.walk(file_dir):     #从总文件夹（具体到科目）开始找
        fpath = root.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        if len(fpath) == 14:
            if transfer_time(fpath[1:11]) >= time_start and transfer_time(fpath[1:11])<=time_end:
                # print(fpath)    #找到文件目录，并解压文件\
                for number in range(7):
                    # try:
                    print('read_path')
                    print(os.getcwd() + '/{}'.format(name)+fpath+'/response-{}'.format(number+1))
                    for roots, dirss, filess in os.walk(os.getcwd() + '/{}'.format(name)+fpath+'/response-{}'.format(number+1)):
                        writtn_num = 0
                        unwritten_num = 0
                        print(len(filess))
                        # print('{}/{}/{}/{}_f_path.txt'.format(os.getcwd(),name,fpath,name))
                        with open('{}/{}/{}/{}_f_path.txt'.format(os.getcwd(),name,fpath,name),'a',encoding='utf-8')as f_path:
                            with open('{}/{}/{}/{}_f_score.txt'.format(os.getcwd(),name,fpath,name),'a',encoding='utf-8')as f_score:
                                with open('{}/{}/{}/{}_f_text.txt'.format(os.getcwd(),name,fpath,name),'a',encoding='utf-8')as f_text:
                                    print ('read something')
                                    for json_file in filess:
                                        with open(os.getcwd() + '/{}'.format(name)+fpath+'/response-{}/'.format(number+1)+json_file, 'r',encoding='utf-8')as f:   #找到score和ID
                                            f = js.load(f)
                                            if writeen_mark == 0:
                                                f_text.write('#!MLF!#\n')
                                            writeen_mark = 1
                                            try:
                                                x = f['result']['overall']
                                            except:
                                                # f['result']['overall'] = str(1001)
                                                continue
                                            if f['result']['overall'] != str(1001):
                                                f_score.write(f['recordId'] + '.wav ')
                                                f_score.write(str(f['result']['overall'])+' ')
                                                f_score.write(str(f['result']['res'])+' ')
                                                f_score.write(str(f['params']['param']['request']['coreType'])+ '\n')
                                                f_text.write('"*' + f['recordId'] + '.lab"\n')
                                                f_text.write(f['params']['param']['request']['refText'] + '\n')
                                            if len(fpath) == 14:
                                                f_path.write(os.getcwd() + '/{}/'.format(name) +fpath+ f['recordId'] + '.wav' + '\n')
                                            else:
                                                None
                                            print('写入的数量：{}'.format(writtn_num))
    return 'finish'

def transfer_time(time_):
    """
    将输入的时间格式化
    :param time_:
    :return:
    """
    time_ = time_.replace('-','')
    if time_[4] == str(0):
        if time_[6] == str(0):
            time_ = date(int(time_[0:4]), int(time_[5]), int(time_[7]))
        else:
            time_ = date(int(time_[0:4]), int(time_[5]), int(time_[6:8]))
    else:
        if time_[6] == str(0):
            time_ = date(int(time_[0:4]), int(time_[4:6]), int(time_[7]))
        else:
            time_ = date(int(time_[0:4]), int(time_[4:6]), int(time_[6:8]))
    return time_
if __name__ == '__main__':
    # time_start = date(2019, 4, 18)
    # time_end = date(2019, 4, 22)
    name = sys.argv[3]
    print('current path:')
    print(os.getcwd())
    startdir = '/root/audio/{}'.format(name)
    # startdir = '/data/workspace/ENAudios/evl/xiansheng/{}'.format(name)
    audio_list = ['audio-1.tar.gz']
    index_list = ['index-1.txt.tar.gz']
    response_list = [ 'response-1.tar.gz',]
    if name == 'peiyouips':
        for i in range(2,9):
            audio_list.append('audio-{}.tar.gz'.format(i))
            index_list.append('index-{}.tar.gz'.format(i))
            response_list.append('response-{}.tar.gz'.format(i))
    time_start = transfer_time(sys.argv[1])
    time_end = transfer_time(sys.argv[2])
    print(utar_all(startdir))