import pickle
import os
import numpy as np
import csv
from sklearn import preprocessing
import pandas as pd

rootdir = '/home/shixiaohan-toda/Documents/DataBase/Three-Layer_Data/Deep3L0908/'
print(rootdir)
fea_name = 'melSpec_Deep3L'
fea_file = rootdir + fea_name
label_name = 'Multi-Semant-Dimens-Ori.xlsx'
label_file = rootdir + label_name

def Get_fea(dir):
    traindata = []
    num = 0
    for sess in os.listdir(dir):
        data_dir = dir + '/' + sess
        data_1 = []
        data = {}
        file = open(data_dir, 'r')
        file_content = csv.reader(file)
        for row in file_content:
            x = []
            for i in range(len(row)):
                row[i] = float(row[i])
                b = np.isinf(row[i])
                # print(b)
                if b:
                    print(row[i])
                x.append(row[i])
            row = np.array(x)
            data_1.append(row)
        data['id'] = sess[:-4]
        data_1_1 = np.array(data_1)
        data['fea_data'] = data_1_1.T
        num = num + 1
        traindata.append(data)
        print(num)
    print(len(traindata))
    return traindata


def Get_label(label_file):
    df = pd.read_excel(label_file)
    data = df.values
    #print("获取到所有的值:\n{}".format(data))
    train_label = []
    for i in range(len(data)):
        s_data = {}
        s_data['Utterance'] = data[i][0]
        s_data['speaker_idx'] = data[i][1]
        s_data['Langtype'] = data[i][2]
        s_data['Cat'] = data[i][3]
        s_data['idx'] = data[i][4]
        s_data['Group'] = data[i][5]

        s_data['1_Bright'] = data[i][6]
        s_data['2_Dark'] = data[i][7]
        s_data['3_High'] = data[i][8]
        s_data['4_Low'] = data[i][9]
        s_data['5_Strong'] = data[i][10]
        s_data['6_Weak'] = data[i][11]
        s_data['7_Calm'] = data[i][12]
        s_data['8_Unstable'] = data[i][13]
        s_data['9_Well-modulated'] = data[i][14]
        s_data['10_Monotonous'] = data[i][15]
        s_data['11_Heavy'] = data[i][16]
        s_data['12_Clear'] = data[i][17]
        s_data['13_Noisy'] = data[i][18]
        s_data['14_Quiet'] = data[i][19]
        s_data['15_Sharp'] = data[i][20]
        s_data['16_Fast'] = data[i][21]
        s_data['17_Slow'] = data[i][22]

        s_data['Data_label'] = data[i][6:23]

        s_data['1_Valence'] = data[i][23]
        s_data['2_Activation'] = data[i][24]
        train_label.append(s_data)
    return train_label

def Class_data(all_data,All_label):
    for i in range(len(All_label)):
        for j in range(len(all_data)):
            print(all_data[j]['id'])
            print(All_label[i]['Utterance'])
            if(all_data[j]['id'] == All_label[i]['Utterance']):
                All_label[i]['fea_data'] = all_data[j]['fea_data']
    return All_label

all_data = Get_fea(fea_file)
All_label = Get_label(label_file)
All_data_class = Class_data(all_data,All_label)

#list_train = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
list_train = [1,2,3,4,5,6,7,8,9,10]

#train_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
train_data = [[],[],[],[],[],[],[],[],[],[]]
for i in range(len(All_data_class)):
    train_data[All_data_class[i]['Group']-1].append(All_data_class[i])

file = open('train_data.pickle', 'wb')
pickle.dump(train_data,file)
file.close()

'''
for i in range(len(All_label)):
    for j in range(len(All_label[i])):
        fea = []
        for x in range(len(All_data_class[i])):
            if(str(j+1) == str(All_data_class[i][x]['time_class'])):
                fea.append(All_data_class[i][x]['fea_data'])
        All_label[i][j]['ALL_fea_data'] = fea
        print(j)

a = [0.0 for i in range(5)]
a = np.array(a)

lens = []
for i in range(len(All_label)):
    for j in range(len(All_label[i])):
        ha = []
        if(len(All_label[i][j]['ALL_fea_data']) < 5):
            for z in range(len(All_label[i][j]['ALL_fea_data'])):
                ha.append(np.array(All_label[i][j]['ALL_fea_data'][z]))
            len_zero = 5 - len(All_label[i][j]['ALL_fea_data'])
            for x in range(len_zero):
                ha.append(a)
        else:
            for z in range(len(All_label[i][j]['ALL_fea_data'])):
                if(z < 5):
                    ha.append(np.array(All_label[i][j]['ALL_fea_data'][z]))
        All_label[i][j]['ALL_fea_data'] = ha


train_data = []
test_data = []
for i in range(len(All_label)):
    if(All_label[i][0]['id'][0] == 't'):
        train_data.append(All_label[i])
    if (All_label[i][0]['id'][0] == 'd'):
        test_data.append(All_label[i])

print(len(train_data))
print(len(test_data))

print(train_data[0][:5])
print(test_data[0][:5])
file = open('train_data.pickle', 'wb')
pickle.dump(train_data,file)
file.close()
file = open('test_data.pickle', 'wb')
pickle.dump(test_data,file)
file.close()
'''
