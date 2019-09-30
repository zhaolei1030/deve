# -*- coding: UTF-8 -*-
import cv2
import os
import sys
import subprocess
import logging
import shutil
import datetime
import numpy as np

#去模糊功能实现的类函数

def pre_img_pro(img):
    """返回图片灰度图和resize后的图片"""
    img = cv2.imread(img)  # 读取图片
    reImg = cv2.resize(img, (800, 900), interpolation=cv2.INTER_CUBIC)  #
    img2gray = cv2.cvtColor(reImg, cv2.COLOR_BGR2GRAY)  # 将图片压缩为单通道的灰度图
    return img2gray, reImg

def get_score(img_matrix):
    """用get_matrix（）和pre_img_pro（）函数得到图片"""
    img2gray, reImg = pre_img_pro(img_matrix)
    f  = np.matrix(img) / 255.0
    x_1 = f[1:, :-1]
    y_1 = f[:-1, :-1]
    x_2 = f[:-1, 1:]
    ab1 = np.abs(x_1 - y_1)
    ab2 = np.abs(x_2 - y_1)
    summary = np.multiply(ab1, ab2)
    score = np.sum(summary)
    return score
def clean_Data(ori_file_path,dir_file_path):
    """比较参数，若小于100则定义为模糊图片，将模糊图片移除文件夹"""
    img_list = os.listdir(ori_file_path)
    vague_number = 0
    for img in img_list:
        img = ori_file_path + img
        print(img)
        score = get_score(img)
        if score < 150:
            shutil.move(img, dir_file_path)
            vague_number += 1
    return vague_number

if __name__ == '__main__':
    command = 'ls /workspace/nb_data/all'
    r = os.popen(command)
    info = r.readlines()  # 读取命令行的输出到一个list
    total_vague_number = 0
    for dir in info:  # 按行遍历
        dir = dir.strip('\r\n')
        print(dir)
        img_file = "path/{}/".format(dir)
        new_path = "path/{}/dup_data/".format(dir)
        if not os.listdir(img_file) == []:
            try:
                num = clean_Data(img_file, new_path)
                total_vague_number += num
            except:
                None
        # os.system('mv {} /workspace/nb_data/cleaned_data/'.format(img_file))
    with open('path/name.txt','a+')as f:
        f.write('vague:{}'.format(total_vague_number))
        f.write('\n')