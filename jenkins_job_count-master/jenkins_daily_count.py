import jenkins
import time
from datetime import datetime, timedelta, date
import json
import requests
import re
import pymysql

# from .models import Job, BuildInfo, BuildSummary, FailureRule, failure_type_choices, FailureSummary


def count_number(server,job_name,todayTime,yesterdayTime):
    """
    统计构建个数
    :param server:
    :param job_name:任务名称
    :param todayTime:时间
    :param yesterdayTime:时间
    :return:
    """
    global count_y
    global count_t
    # print(job_name["fullname"])
    try:
        t1 = time.time()
        next_build_number = server.get_job_info(job_name["fullname"])['nextBuildNumber']
        number = 0
        for j in range(next_build_number, 0, -1):
            number += 1
            # 根据job名称和job编号, 获取job的构建信息
            build_info = server.get_build_info(job_name["fullname"], j - 1)
            # 取出构建信息, 之后和当日凌晨的时间戳作比较, 如果大于当前日时间戳, count(构建次数)+1, 如果小于, 在他下面的job号直接跳过, 跳到下一次循环
            if  int(build_info["timestamp"]) > int(todayTime()):
                count_t += 1
            if int(build_info["timestamp"]) > int(yesterdayTime()) :
                count_y += 1
                # print(count)
            else:
                break
        if int(time.time()-t1)>= 20:
            print(job_name["fullname"])
            # print('running time:')
            # print(int(time.time()-t1))
        # print(number)
    # print(next_build_number)
    except:
        pass
def get_jenkins_build_count(n):
    """
    通过传参补之前缺失统计信息
    :param n: 之前计算的天数
    :return:
    """
    global count_y
    global count_t
    count_t = 0
    count_y = 0
    now = datetime.now()
    oneday = timedelta(days=1)
    nday = timedelta(days=n)
    today = datetime(now.year, now.month, now.day) - nday
    yesterday = today - oneday
    print(today)
    print(yesterday)
    db = pymysql.connect(host="xxx.xxx.xxx.xx", user="xxxxx", passwd="xxxxx", db="xxxxx",
                         port=000, charset='utf8')
    cursor = db.cursor()
    sql = "select * FROM new_table"
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        while row:
            if row[0] == yesterday:
                return 'have existed'
            row = cursor.fetchone()
        # print(row)
        db.commit()
        # print("done")
    except:
        db.rollback()
    db.close()
    the_begin_date = yesterday
    yesterday_time = int(time.mktime(yesterday.timetuple()))
    today_time = int(time.mktime(today.timetuple()))
    yesterdayTime = lambda: int(round(yesterday_time * 1000))
    todayTime = lambda: int(round(today_time * 1000))

    server = jenkins.Jenkins('http://url', username='xxx', password='xxxxx')
    t2 = time.time()
    for first_level in server.get_all_jobs()[:]:
        # if int(time.time()-t2)>= 20:
            # print('running time：')
            # print(int(time.time()-t2))
        if 'color' in list(first_level.keys()):
            count_number(server, first_level,todayTime,yesterdayTime)
            # print(first_level)
        else:
            for second_level in first_level['jobs']:
                if 'color' in list(second_level.keys()):
                    count_number(server, second_level,todayTime,yesterdayTime)
                else:
                    for third_level in second_level['jobs']:
                        if 'color' in list(third_level.keys()):
                            count_number(server, third_level,todayTime,yesterdayTime)
                        else:
                            for fourth_level in third_level['jobs']:
                                if 'color' in list(fourth_level.keys()):
                                    count_number(server, fourth_level,todayTime,yesterdayTime)
                                else:
                                    for fifth_level in fourth_level['jobs']:
                                        if 'color' in list(fifth_level.keys()):
                                            count_number(server, fifth_level,todayTime,yesterdayTime)
    print(count_y-count_t)
    # 插入mysql数据库
    count = count_y-count_t
    db = pymysql.connect(host="xxx.xxx.xxx.xx", user="xxxxx", passwd="xxxxx", db="xxxxx", port=000, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO  new_table(day ,count )\
            VALUES ('%s', %s)" % \
            (the_begin_date, count)
    try:
        cursor.execute(sql)
        db.commit()
        print("done")
    except:
        db.rollback()
    db.close()


if __name__ == "__main__":
    get_jenkins_build_count(0)