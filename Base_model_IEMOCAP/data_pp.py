'''
Author: error: git config user.name && git config user.email & please set dead value or install git
Date: 2022-11-07 15:09:40
LastEditors: error: git config user.name && git config user.email & please set dead value or install git
LastEditTime: 2022-11-07 15:30:34
FilePath: /Xingfeng_code/Base_model_IEMOCAP/data_pp.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
import re
import numpy as np
import os
import glob
import pickle
import csv
import sys

os.chdir(sys.path[0])

with open('../Speech_data.pickle', 'rb') as file:
    data = pickle.load(file)

train_data = [[],[],[],[],[]]
num = 0
emotion_list = [1,2,3,4,5]
for i in range(len(data)):
    for j in range(len(data[i])):
        if(data[i][j]['label'] in emotion_list):
            if(data[i][j]['label'] == 5):
                data[i][j]['label'] = 2
            data[i][j]['label'] = data[i][j]['label'] - 1
            data[i][j]['spec_data'] = data[i][j]['spec_data'][0]
            train_data[int(data[i][j]['id'][4])-1].append(data[i][j])
            num = num +1
print(num)
#print(len(train_data[0][0]['spec_data'][0][0]))
file = open('train_data.pickle', 'wb')
pickle.dump(train_data, file)
file.close()