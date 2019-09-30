import os
from datetime import date
import time
from dateutil.rrule import rrule, DAILY
import subprocess
import sys
sleep_time = 10
def transfer_time(time_):
    """
    转化时间格式
    :param time_:输入的时间
    :return:
    """
    time_ = time_.replace('-','')
    if time_[4] == str(0):
        if time_[6] == str(0):
            time_start = date(int(time_[0:4]), int(time_[5]), int(time_[7]))
        else:
            time_start = date(int(time_[0:4]), int(time_[5]), int(time_[6:8]))
    else:
        if time_[6] == str(0):
            time_start = date(int(time_[0:4]), int(time_[4:6]), int(time_[7]))
        else:
            time_start = date(int(time_[0:4]), int(time_[4:6]), int(time_[6:8]))
    return time_start

if __name__ == '__main__':
    time_start = date(transfer_time(sys.argv[1]))
    time_end = date(transfer_time(sys.argv[2]))
    user_list = [{'id':'name'}]
    for user in user_list:
        for dt in rrule(DAILY, dtstart=time_start, until=time_end):
            cur_day = dt.strftime("%Y-%m-%d")
            path1 = 'file_path/{}/'.format(user[list(user.keys())[0]])
            if not os.path.exists(path1):
                os.mkdir(path1)
            paths = path1 + cur_day
            print(paths)
            if not os.path.exists(paths):
                os.mkdir(paths)
            for i in range(1,4):
                if not os.path.exists(paths+'/'+str(i)):
                    os.mkdir(paths+'/'+str(i))
                for k in range(1,9):
                    command2 = 'curl ftp://user_name{}:password{}@url/{}/{}/audio-{}.tar.gz -o {}/{}/audio-{}.tar.gz'.format(
                        list(user.keys())[0], list(user.keys())[0], cur_day, i, k,paths, i,k)
                    print(command2)
                    os.system(command2)
                    if not os.path.exists('{}/{}/audio-{}.tar.gz'.format(paths, i,k)):
                        continue

                    command2 = 'curl ftp://user_name{}:password{}@url/{}/{}/index-{}.txt.tar.gz -o {}/{}/index-{}.txt.tar.gz'.format(
                        list(user.keys())[0], list(user.keys())[0], cur_day, i,k, paths, i,k)
                    os.system(command2)
                    command2 = 'curl ftp://user_name{}:password{}@url/{}/{}/response-{}.tar.gz -o {}/{}/response-{}.tar.gz'.format(
                        list(user.keys())[0], list(user.keys())[0], cur_day, i,k, paths, i,k)
                    os.system(command2)
                    for root, dirs, files in os.walk(paths + '/' + str(i)):
                        if files == []:
                            os.rmdir(paths + '/' + str(i))
            if os.listdir(paths) == []:
                os.rmdir(paths)