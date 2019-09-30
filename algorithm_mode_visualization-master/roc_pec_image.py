import os
import io
import time
import codecs
import requests
#在内存中读写二进制
from io import BytesIO
from ftplib import FTP
import base64,math,csv

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
def ftpconnect(host, username, password):
    """
    连接ftp的函数
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
    图片上传ftp的函数
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
def precision_and_recall(gallery_dir ,test_data_dir ,result_path ,thr_min=0 ,thr_max=100, interval=2,score = 0.2):
    """
    计算精准和召回的函数
    :param gallery_dir:
    :param test_data_dir:
    :param result_path:
    :param thr_min: 最小值
    :param thr_max: 最大值
    :param interval: 间隔
    :param score: 评分阈值
    :return:
    """
    os.chdir(result_path)
    class_files = os.listdir('./')
    thr_list = []
    recall_list = []
    thr_recall = []
    ten_thr = []
    thr_FPR = []
    FPR_list = []
    bad_case = []
    for thr in range(thr_min, thr_max, interval):  #遍历结果文件夹
        thr_list.append(thr / 100.0)
        total_hit = 0
        total_mistake = 0
        total_count = 0
        for class_file in class_files:

            f = codecs.open(result_path+class_file+'/'+'id_info.txt','r')
            result = f.readlines()

            createValue = time.time() + 8 * 60 * 60
            T = time.strftime('%Y-%m-%d_%H', time.gmtime(createValue))
            accuracy = recall = fpr = f1_score = 0
            precision = 1
            thr_list.append(thr / 100.0)
            tp = fp = fn = 0
            a = 0
            hit = mistake = count = 0
            FPR = 0
            for r in result:
                v = r.split(',')
                top1 = v[1]
                if float(v[-1]) < score:   #根据阈值取数据
                    bad_case.append(v[0])
                    bad_case.append(v[-1])
                if float(v[-1]) >= thr / 100.0:
                    if v[0].split('/')[-1].split('\\')[0] == top1:
                        hit += 1
                    else:
                        mistake += 1
                        test_img_path = test_data_dir + v[0].split('/')[-2] + '/' + v[0]
                        g_img_path = gallery_dir + v[1]
                count += 1
            total_hit = total_hit + hit
            total_mistake = total_mistake + mistake
            total_count = total_count + count
            # print("class_id:",class_file)
            # print("hit_num: %s ......mistake_num: %s ...... loss_num: %s ...... total_num: %s......" % (
            # hit, mistake, count - hit - mistake, count))

            if hit + mistake != 0:
                precision = hit / float(hit + mistake)
            recall = hit / float(count)
            # FPR = mistake / float(count - hit)
            # print(class_file,precision,recall)

        # print("total_hit_num: %s ......total_mistake_num: %s ...... total_loss_num: %s ...... totaltotal_num: %s......" % (
        if total_hit + total_mistake != 0:
            total_precision = total_hit / float(total_hit + total_mistake)
        else:
            total_precision = 0
        total_recall = total_hit / float(total_count)
        FPR = total_mistake / float(total_count - total_hit)
        # print("Precision:{0:.5f} ......Recall: {1:.5f} ...... ".format(total_precision, total_recall))
        if thr%10==0:
            print ("{}".format(thr/100.0))
            print('total',total_precision, total_recall,total_count)
            ten_thr.append(thr/100.0)
            thr_recall.append(total_recall)
            thr_FPR.append(total_precision)

        recall_list.append(total_recall)
        FPR_list.append(FPR)
    iris_im_1, iris_im_email_1, pic_url= print_ROC('FPR', 'TPR', 'ROC-info', FPR_list,
                                           recall_list)
    # print(len(ten_thr))
    # print(len(thr_FPR))
    # print(len(thr_recall))
    print_recall('threshold', 'rate', 'recall', thr_recall, thr_FPR,ten_thr)
    # print(len(FPR_list))
    # print(len(recall_list))
    produce_html(bad_case)

def print_ROC(x_name, y_name,pic_name,FPR,TPR):     #画图并上传ftp
    """
    画ROC的图
    :param x_name: 横轴名字
    :param y_name: 纵轴名字
    :param pic_name: 待命名图片名字
    :param FPR:FPR数组
    :param TPR:TPR数组
    :return:
    """
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(pic_name)
    # print(FPR)
    # print(TPR)
    plt.plot(FPR,TPR,"x-",label="ROC",color='darkblue')
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.grid(True)
    plt.savefig('path\\' + pic_name + '.png', dpi=1000)
    # ftp = ftpconnect('xxx.xxx.xxx.x', 'xx', 'xxxxx')
    # uploadfile(ftp, '/path/{}.png'.format(pic_name), 'local_path\\' + name + '.png')
    # time.sleep(3)
    pic_url = 'http://xxx.xxx.xxx.x/path/{}.png'.format(pic_name)
    buffer = BytesIO()
    plt.show()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb_1 = base64.b64encode(plot_data)
    ims_1 = imb_1.decode()
    imd_1 = "data:image/png;base64," + ims_1
    iris_im_email_1 = """<h1>""" + pic_name + """</h1>  """ + """<img src="%s">""" % imd_1
    iris_im_1 = """<h1>""" + pic_name + """</h1>  """ + """<img src=""" + pic_name + """.png width=640 height=480/> """
    plt.close('all')
    return iris_im_1, iris_im_email_1, pic_url
def print_recall(x_name, y_name,pic_name,recall,pre,thr):
    """
    画recall的图
    :param x_name: 横轴名字
    :param y_name: 纵轴名字
    :param pic_name: 图片名字
    :param recall: 召回率的数组
    :param pre: 百分比
    :param thr: thread数组
    :return:
    """
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(pic_name)
    plt.plot(thr,recall,"x-",label="recall",color='darkorange')
    plt.plot(thr,pre,"x-",label="pre",color='darkblue')
    plt.legend(bbox_to_anchor=(1.0, 1), loc=1, borderaxespad=0.)
    plt.grid(True)
    plt.savefig('path\\' + pic_name + '.png', dpi=1000)
    pic_url = 'http://xxx.xxx.xxx.x/path/{}.png'.format(pic_name)
    buffer = BytesIO()
    plt.show()
    plt.savefig(buffer)
    return  pic_url
def produce_html(case_list): # 基于模板，创建html页面
    mark = 1
    with io.open(r'path\name.html', 'r', encoding='utf-8') as f1:
        with io.open(r'path\new_name.html', 'w', encoding='utf-8') as f2:
            for i in f1:
                if mark == 1:
                    if i.startswith('            <b><font color="red"'):
                        f2.write(u'            <b><font color="red" size="6">Result: </font></b>  <hr size="2" width="100%"  /></td>  </tr>')
                        mark = 0
                    else:
                        f2.write(i)
                else:
                    f2.write(
                        '          <table cellpadding="0" cellspacing="0"  border="1" align="center"><tr><font size="4">' + '\n')
                    f2.write(
                        '					<tr><td>path</td><td>predict rate</td></tr>' + '\n')
                    if i.startswith('						<tr><td>start'):
                        for unit in range(int(len(case_list)/2)):
                            f2.write(u'						<tr><td>{}</td><td>{}</td></tr>'.format(case_list[unit*2],case_list[unit*2+1])+'\n')
                            mark = 1

                        f2.write(
                                u'	<div align="center"><img src="path\\pic_name.png" align="center" width="600" height="600" />' + '\n')
                        f2.write(
                                u'	<div align="center"><img src="path\\pic_name.png" align="center" width="600" height="600" />' + '\n')
                    else:
                        f2.write('\n</table>')
                    mark = 1
                    None

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

if __name__ == '__main__':
    gallery_dir = 'xxx\\'
    test_data_dir = 'xxx\\'
    result_path = 'xxx\\'
    precision_and_recall(gallery_dir ,test_data_dir ,result_path)

