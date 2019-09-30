import os
import subprocess
import time
import json as js
import io
from string import Template
import random
import matplotlib.pyplot as plt
import numpy as np
def getDateTime():
    return time.strftime(r'%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
#引入传入环境变量的参数
thread = int(os.environ['start_num'])
adding_number = int(os.environ['step'])
JmxTemlFileName = os.environ['JmxFileName']
duration = int(os.environ['duration'])
error_rate = float(os.environ['error_rate'])
min_range = int(os.environ['min_range'])
name = getDateTime()
end_num = int(os.environ['end_num'])
global sleeptime
sleeptime = int(os.environ['sleeptime'])
#为新的jmx文件测试结果创建文件夹
if not os.path.exists('/root/autotest/file_saver/'+name):
    os.mkdir('/root/autotest/file_saver/'+name)
currpath = '/root/autotest/file_saver/'+name

# JmxTemlFileName = '/root/Downloads/result.jmx'

JMETER_Home = '/root/autotest/files/jm/apache-jmeter-5.1.1/bin/jmeter.sh'

global error_status, max_th, min_th,total_info,flag,threads_list, per_99_list,per_95_list, transaction,length
error_status = 0
total_info,threads_list, per_99_list,per_95_list,transaction, per_50_list = [], [], [], [], [], []
flag,length = 0, 0
max_th, min_th = int(os.environ['start_num']), int(os.environ['start_num'])
#交互式执行jmeter进行压测，便于出错调试和监控
def execcmd(command,error_rate):
    """
    执行cmd进行测试，返回结果
    :param command:
    :param error_rate:
    :return:
    """
    global error_status
    global flag
    error_status = 0
    print(command)
    output = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True, universal_newlines=True)
    stderrinfo, stdoutinfo = output.communicate()
    print(stderrinfo)
#执行压测
def execjmxs(JmxTemlFileName ,Num_Threads,error_rate , Duration = 60):
    """
    写新的jmx文件，并对特定的jmx文件进行压测
    :param JmxTemlFileName:
    :param Num_Threads:
    :param error_rate:
    :param Duration:
    :return:
    """
    global error_status
    error_status = 0
    Num_Threads = int(Num_Threads)
    tmpstr = ''
    global htmlreportpath, csvfilename, tmpjmxfile
    with io.open(JmxTemlFileName, "r", encoding="utf-8") as file:
        now = getDateTime()
        tmpjmxfile = currpath + r"/T{}-{}XL.jmx".format(
            Num_Threads,now)
#依据原有jmx文件生成新的jmx文件
        with io.open(tmpjmxfile, "w", encoding="utf-8") as files:
            # files.writelines(i)
            for i in file:
                # if i.startswith('          <stringProp name="LoopController.loops">'):
                #     files.writelines('          <stringProp name="LoopController.loops">{}</stringProp>'.format(Loops))
                if i.startswith('        <stringProp name="ThreadGroup.num_threads">'):
                    files.writelines(u'        <stringProp name="ThreadGroup.num_threads">{}</stringProp>'.format(Num_Threads))
                elif i.startswith('        <stringProp name="ThreadGroup.duration">'):
                    files.writelines(u'        <stringProp name="ThreadGroup.duration">{}</stringProp>'.format(Duration))
                else:
                    files.writelines(i)
    tmpjmxfile = currpath + r"/T{}-{}XL.jmx".format(Num_Threads,now)
    with io.open(tmpjmxfile, "a", encoding="utf-8") as file:
        file.writelines(tmpstr)
    csvfilename = currpath + "/{}-{}.jtl".format(Num_Threads,now)
    htmlreportpath = currpath + "/{}-{}htmlreport".format(Num_Threads,now)
    if not os.path.exists(htmlreportpath):
        os.makedirs(htmlreportpath)
    t1 = time.time()
#命令行调用jmeter进行压测
    execjmxouthtml = "{} -n -t {} -l {} -e -o {}".format(JMETER_Home,tmpjmxfile,csvfilename ,htmlreportpath)
    execcmd(execjmxouthtml,error_rate)
    print('succeed')
#对下一步压测并发数进行调整的逻辑
def start_pro(JmxTemlFileName, thread, adding_number, minimum_range,error_rate, end_num, duration = 180, repeated_num = 3, increase_rate = 0.05):
    """
    传入压测参数进行压测
    :param JmxTemlFileName:
    :param thread:
    :param adding_number:
    :param minimum_range:
    :param error_rate:
    :param end_num:
    :param duration:
    :param repeated_num:
    :param increase_rate:
    :return:
    """
    global error_status,total_info,flag,min_th,max_th, length
    passed_thread1 = thread
    passed_thread2 = 0
    last_tps,mark_tps = 0, 0
    time_list = []
    temp_transaction = []
    temp_thread = []
    while True:
        last_status = error_status
        start_time = time.strftime(r'%m-%d-%H-%M-%S', time.localtime(time.time()))
        execjmxs(JmxTemlFileName, thread, error_rate, duration)
        #读取json结果到内存
        with open('{}/statistics.json'.format(htmlreportpath), 'r')as f:
            #计算50per分位数
            with io.open(csvfilename, encoding='utf-8')as f1:
                for i in f1:
                    list1 = i.split(',')
                    try:
                        time_list.append(int(list1[1]))
                    except:
                        None
                time_list.sort()
                f = js.load(f)
                if len(f) == 2:
                    length = 1
                    k = list(f.keys())[1]
                    total_info.append({k:[round(int(f[k]['sampleCount']),2),round(int(f[k]['meanResTime']),2),round(int(f[k]['pct1ResTime']),2),round(int(f[k]['pct2ResTime']),2),round(int(f[k]['pct3ResTime']),2),round(int(f[k]['throughput']),2),'%.2f'%float(f[k]['errorPct']), int(thread),time_list[int(len(time_list)/2)],start_time]})
                    tps = round(int(f[k]['throughput']),2)
                    err = float(f[k]['errorPct'])
                    temp_transaction.append(tps)
                    temp_thread.append(int(thread))
                else:
                    length = len(f)
                    for k in f:
                        total_info.append({k: [round(int(f[k]['sampleCount']), 2), round(int(f[k]['meanResTime']), 2),
                                               round(int(f[k]['pct1ResTime']), 2), round(int(f[k]['pct2ResTime']), 2),
                                               round(int(f[k]['pct3ResTime']), 2), round(int(f[k]['throughput']), 2),
                                               '%.2f'%float(f[k]['errorPct']), int(thread),time_list[int(len(time_list)/2)], start_time]})
                        tps = round(int(f[k]['throughput']), 2)
                        err = float(f[k]['errorPct'])
                        temp_transaction.append(tps)
                        temp_thread.append(int(thread))
        print('err  {}'.format(err))
        print('error_rate   {}'.format(error_rate))
        time.sleep(sleeptime)
        target_th = thread
        #判断下一步该如何调整线程数
        #当出错后，接下来每一次上升和下降的都会线程数减半
        if err > error_rate:
            error_status = 1
            flag += 1
        if tps < last_tps*(1+increase_rate):
            mark_tps += 1
        else:
            mark_tps = 0
            last_tps = tps
        if mark_tps >= repeated_num:
            # target_th = temp_thread[temp_transaction.index(max(temp_transaction))]
            # mark_tps = 99
            break
        if adding_number < minimum_range:
            break
        if thread > end_num:
            break
        if flag == 0:
            thread += adding_number
        #passed变量用于将当前状态保留至下一轮，供输出范围时比较。
        else:
            if error_status == 0:
                passed_thread2 = int(thread)
                adding_number = adding_number / 2
                thread += adding_number
            else:
                passed_thread1 = int(thread)
                adding_number = adding_number / 2
                thread -= adding_number
                error_status = 0
        if int(thread) <= 0:
            break
        if flag == 0:            #the last upward and downward threads is related to the last two duild
            min_th = passed_thread2
            max_th = int(thread)
        else:
            if last_status == 0:
                if error_status == 0:
                    min_th = int(thread)
                    max_th = passed_thread1
                else:
                    max_th = int(thread)
                    min_th = passed_thread2
            else:
                if error_status == 0:
                    min_th = int(thread)
                    max_th = passed_thread1
                else:
                    max_th = int(thread)
                    min_th = passed_thread2
    return flag, target_th, mark_tps
#plt画图
def draw(unit,names):
    """
    画图程序，画每日状态趋势图
    :param unit:
    :param names:
    :return:
    """
    global threads_list, per_95_list, per_99_list, transaction, per_50_list
    new_per_95_list, new_per_99_list,new_transaction,new_per_50_list = [], [], [], []
    binary_mark = 0
    for i in sorted(threads_list):
        new_per_95_list.append(per_95_list[threads_list.index(i)])
        new_per_99_list.append(per_99_list[threads_list.index(i)])
        new_per_50_list.append(per_50_list[threads_list.index(i)])
        new_transaction.append(transaction[threads_list.index(i)])
    if int(new_transaction[0]) / int(new_per_99_list[0]) > 10:
        new_transaction = [l/20 for l in new_transaction]
        binary_mark = 1
    x = np.array(sorted(threads_list))
    y1 = np.array(new_per_95_list)
    y2 = np.array(new_per_99_list)
    y3 = np.array(new_transaction)
    y4 = np.array(new_per_50_list)
    plt.figure(figsize=(8, 8), dpi=80)
    plt.title('{} Trend Chart'.format(names))
    plt.plot(x, y1, label="95per", linewidth=2, color='blue')
    plt.plot(x, y2, label='99per', linewidth=2, color='red')
    plt.plot(x, y4, label='50per', linewidth=2, color='green')
    if binary_mark == 1:
        plt.plot(x, y3, label='TPS(数量为TPS/10)', linewidth=2, color='black')
    else:
        plt.plot(x, y3, label='TPS', linewidth=2, color='black')
    plt.plot()
    plt.xlabel('Threads', size=15)
    plt.ylabel('Number', rotation=0, size=15)
    plt.legend()
    plt.savefig('/root/workspace/workspace/EP/TestGenie/AutoLoad/auto_pressure_test/yixiu_trend_{}.png'.format(unit))
#基于模板生成新的html
def produce_html():
    """
    生成html报告
    :return:
    """
    global total_info,threads_list,per_95_list,per_99_list,transaction,per_50_list,length,min_th,max_th,flag
    del threads_list[:], per_95_list[:], per_99_list[:], transaction[:], per_50_list[:]
    mark = 1
    with io.open(r'/root/autotest/Original_file/web_page.html', 'r', encoding='utf-8') as f1:
        with io.open(r'//root/autotest/report/new_report.html', 'w', encoding='utf-8') as f2:
            for i in f1:
                if mark == 1:
                    if i.startswith('            <b><font color="red"'):
                        if flag == 0:
                            f2.write(u'            <b><font color="red" size="6" >Estimated Max Concurrent Threads: {} Threads</font></b>'.format(int(max_th)))
                        else:
                            f2.write(
                                u'            <b><font color="red" size="6" >Estimated Max Concurrent Threads: {}~{} Threads</font></b>'.format(
                                    int(min_th), int(max_th)))
                        mark = 0
                    else:
                        f2.write(i)
                else:
                    for unit in range(length):
                        task_name = ''
                        # print(length)
                        # print(len(total_info)/length)
                        total_units = [total_info[x*length + unit] for x in range(int(len(total_info)/length))]
                        # print(total_units)
                        f2.write('          <table cellpadding="0" cellspacing="0"  border="1" align="center"><tr><font size="4">'+'\n')
                        f2.write('					<tr><td>开始时间</td><td>Label</td><td>并发数</td><td>Sample</td><td>Average</td><td>50th pct</td><td>90th pct</td><td>95th pct</td><td>99th pct</td><td>TPS</td><td>errorPct</td></tr>'+'\n')
                        if i.startswith('						<tr><td>start'):
                            for j in range(len(total_units)):
                                for k in total_units[j]:      #len(total_info[j]) = 1
                                    f2.write(
                                        u'						<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr></tr></font>'
                                            .format(total_units[j][k][9],k, total_units[j][k][7],total_units[j][k][0], total_units[j][k][1], total_units[j][k][8],total_units[j][k][2],
                                                    total_units[j][k][3], total_units[j][k][4], total_units[j][k][5],
                                                    total_units[j][k][6])+ '\n')
                                    threads_list.append(total_units[j][k][7])
                                    per_95_list.append(total_units[j][k][3])
                                    per_99_list.append(total_units[j][k][4])
                                    transaction.append(total_units[j][k][5])
                                    per_50_list.append(total_units[j][k][1])
                                    task_name = k
                            f2.write('\n</table>')
                            f2.write(u'	<div align="center"><img src="/job/EP/job/TestGenie/job/AutoLoad/job/auto_pressure_test/ws/yixiu_trend_{}.png" align="center" width="600" height="600" />'.format(unit)+'\n')
                            mark = 1
                        else:
                            None
                        draw(unit,task_name)
    return None
if __name__ == "__main__":
    detect_tps, target_th, mark_tps = start_pro(JmxTemlFileName,thread, adding_number, min_range,error_rate, end_num,duration)
    produce_html()
    move_command = 'mv {} /root/workspace/workspace/EP/auto_pressure_test'.format(currpath)
    os.system(move_command)
    del_command = 'rm -rf {}'.format(currpath)
    os.system(del_command)