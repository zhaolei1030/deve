from PIL import ImageGrab
from PIL import Image
import sys
import os
import time
from datetime import datetime
import threading
import sys
interval = sys.argv[1]
thread = sys.argv[2]
run_time = sys.argv[3]
pic_num = 0
def getDiff(width, high, image):
    """
    将要裁剪成w*h的image照片 得到渐变序列
    :param width:
    :param high:
    :param image:
    :return:
    """
    diff = []
    im = image.resize((width, high))
    imgray = im.convert('L')  # 转换为灰度图片 便于处理
    pixels = list(imgray.getdata())  # 得到像素数据 灰度0-255

    for row in range(high):
        rowStart = row * width  # 起始位置行号
        for index in range(width - 1):
            leftIndex = rowStart + index  # 当前位置号
            rightIndex = leftIndex + 1
            diff.append(pixels[leftIndex] > pixels[rightIndex])
    return diff


def getHamming(diff=[], diff2=[]):
    """
    得到汉明距离函数
    :param diff:
    :param diff2:
    :return:
    """
    hamming_distance = 0
    for i in range(len(diff)):
        if diff[i] != diff2[i]:
            hamming_distance += 1
    return hamming_distance

def git_pic():
    """
    为图片重命名
    :return:
    """
    name = str(datetime.now() - t1).split('.')
    name = name[0].replace(':', '-')
    images_path = os.getcwd()
    im = ImageGrab.grab()
    im.save(images_path + '\\{}.png'.format(name))
    return None
def sleepp():
    time.sleep(2)

if __name__ == "__main__":
    t1 = datetime.now()
    times = int(float(run_time)*60/int(interval))+1
    for i in range(times):

        # print(name)
        t = threading.Thread(target=git_pic)
        t.start()
        pic_num += 1
        # print(str(datetime.now()-t1))
        # t1 = datetime.now()
        time.sleep(5)
        # t2 = datetime.now()
        # print(str(t2 - t1))
    width = 20
    high = 20
    images_path = os.getcwd()
    video_dir_path = os.listdir(images_path)
    if not os.path.exists(images_path + '/duplicate'):
        os.mkdir(images_path + '/duplicate')
    allDiff = []
    cnt = 0
    []
    for pic in video_dir_path:
        cnt += 1
        # print cnt
        # 文件后缀类型过滤
        if str(pic).split('.')[-1] in ['jpg', 'png']:
            # print ('%s/%s' % (dir_img, str(i)))
            im = Image.open(pic)
            diff = getDiff(width, high, im)
            # print(pic)
            allDiff.append((images_path + '/'+pic, diff))
            # print(allDiff)
    dup_pic = []
    for i in range(len(allDiff)-1):
        ans = getHamming(allDiff[i][1], allDiff[i+1][1])
        print(ans)
        if ans < int(thread):
            dup_pic.append(allDiff[i][0])
            dup_pic.append(allDiff[i+1][0])
    for pic in set(dup_pic):
        os.system('mv {} {}'.format(pic, images_path + '/duplicate'))
    dup_pic = len(set(dup_pic))
    with open('report.txt','w') as f:
        f.write('卡顿检测运行时长：{}分钟\n'.format(run_time))
        f.write('截图时间间隔：{}s\n'.format(interval))
        f.write('截图数量：{}张\n'.format(pic_num))
        f.write('疑似卡顿点：{}个\n'.format(dup_pic))