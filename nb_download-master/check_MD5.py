import hashlib
import datetime
import requests
import time
import os
import argparse
import shutil
import paramiko
#from lxml import etree
print ("downloading with requests")
def auto_rotate(path):
    """路径下全部图片旋转函数"""
    dir_path = path
    object_path = path
    files_path = os.listdir(dir_path)
    count = 0
    for file_path in files_path:
        try:
            sufix = file_path.split('.')[-1].lower()
            if sufix == 'jpg' or sufix == 'jpeg' or sufix == 'png':
                file_name = os.path.join(dir_path, file_path)
                img = cv2.imread(file_name)
                output_path = os.path.join(object_path, file_path)
                cv2.imwrite(output_path, img)
                count += 1
            else:
                file_name = os.path.join(dir_path, file_path)
        except Exception as e:
        #     print('当前文件{}出现问题，Error：{}'.format(file_name, e))
              continue
        finally:
            pass
    print(type(count))
    return int(count)

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    total = 0
    info = os.listdir('path')  # 读取命令行的输出到一个list
    total_rorate_number = 0
    total_dup_number = 0
    for dir in info:  # 按行遍历
        dir = dir.strip('\r\n')
        # dir = str(dir, encoding="utf-8")
        print(dir)
        filepath = "path/{}/".format(dir)
        new_path = "path/{}".format(dir)
        if not os.path.exists(new_path):
            os.system('mkdir {}'.format(new_path))
        if not os.path.exists(new_path+'/dup_data/'):
            os.system('mkdir {}'.format(new_path+'/dup_data/'))
        if not os.path.exists(new_path+'/no_question_data/'):
            os.system('mkdir {}'.format(new_path+'/no_question_data/'))
        if not os.path.exists(new_path+'/unknown_err_data/'):
            os.system('mkdir {}'.format(new_path+'/unknown_err_data/'))
        MD5_list = []
        img_name_list = []
        img_set_list = []
        files = os.listdir(filepath)
        count_whole_img = len(files)
        total += count_whole_img
      #  print(img_set_list)

        print('this is rotate number')
        print(auto_rotate)
        endtime = datetime.datetime.now()
        datadeal_data = endtime - starttime
    with open('path/statistic_info.txt','w')as f:
        f.write('total:{}'.format(total))
        f.write('\n')
        f.write('rorate:{}'.format(total_rorate_number))
        f.write('\n')
    print('rorate finished')