import os
import time
import random
import sys
import argparse
import pickle
import copy
import torch
import numpy as np
import torch.utils.data as Data
import torch.nn.utils.rnn as rmm_utils
import torch.utils.data.dataset as Dataset
import torch.optim as optim
from utils import Get_data
from torch.autograd import Variable
from models import Utterance_net, Output_net
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import recall_score
from sklearn.model_selection import KFold
import sys

os.chdir(sys.path[0])

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
torch.backends.cudnn.enabled = False

with open('train_data.pickle', 'rb') as file:
    data = pickle.load(file)

parser = argparse.ArgumentParser(description="RNN_Model")
parser.add_argument('--cuda', action='store_false')
parser.add_argument('--bid_flag', action='store_false')
parser.add_argument('--batch_first', action='store_false')
parser.add_argument('--batch_size', type=int, default=64, metavar='N')
parser.add_argument('--log_interval', type=int, default=10, metavar='N')
parser.add_argument('--dropout', type=float, default=0.5)
parser.add_argument('--epochs', type=int, default=30)
parser.add_argument('--lr', type=float, default=1e-3)
parser.add_argument('--optim', type=str, default='Adam')
parser.add_argument('--seed', type=int, default=1111)
parser.add_argument('--dia_layers', type=int, default=2)
parser.add_argument('--hidden_layer', type=int, default=256)
parser.add_argument('--out_class', type=int, default=4)
parser.add_argument('--utt_insize', type=int, default=120)
args = parser.parse_args()

torch.manual_seed(args.seed)


def Train(epoch):
    train_loss = 0
    utt_net.train()
    line_net.train()
    for batch_idx, (data_1, target) in enumerate(train_loader):
        if args.cuda:
            data_1, target = data_1.cuda(), target.cuda()
        data_1, target = Variable(data_1), Variable(target)
        target = target.squeeze()
        utt_optim.zero_grad()
        line_optim.zero_grad()
        data_1 = data_1.squeeze()
        utt_out = utt_net(data_1)
        out_put = line_net(utt_out)
        loss = torch.nn.CrossEntropyLoss()(out_put, target.long())

        loss.backward()

        utt_optim.step()
        line_optim.step()
        train_loss += loss

        if batch_idx > 0 and batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * args.batch_size, len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), train_loss.item() / args.log_interval
            ))
            train_loss = 0


def Test(test_len):
    utt_net.eval()
    line_net.eval()
    label_pre = []
    label_true = []
    with torch.no_grad():
        for batch_idx, (data_1, target) in enumerate(test_loader):
            if args.cuda:
                data_1, target = data_1.cuda(), target.cuda()
            data_1, target = Variable(data_1), Variable(target)
            utt_optim.zero_grad()
            line_optim.zero_grad()
            data_1 = data_1.squeeze(0)
            utt_out = utt_net(data_1)
            out_put = line_net(utt_out)
            output = torch.argmax(out_put, dim=1)
            label_true.extend(target.cpu().data.numpy())
            label_pre.extend(output.cpu().data.numpy())
        accuracy_recall = recall_score(label_true[:test_len], label_pre[:test_len], average='macro')
        accuracy_f1 = metrics.f1_score(label_true[:test_len], label_pre[:test_len], average='macro')
        CM_test = confusion_matrix(label_true[:test_len], label_pre[:test_len])
        print(accuracy_recall)
        print(accuracy_f1)
        print(CM_test)
    return accuracy_f1, accuracy_recall, label_pre[:test_len], label_true[:test_len]


Final_result = []
Fineal_f1 = []
result_label = []
kf = KFold(n_splits=5)
load_name = '1'
for index, (train, test) in enumerate(kf.split(data)):
    print(index)
    train_loader, test_loader, input_test_data_id, input_test_label_org, test_len = Get_data(data, train, test, args)
    utt_net = Utterance_net(args.utt_insize, args.hidden_layer, args.out_class, args)
    line_net = Output_net(17,args)
    if args.cuda:
        utt_net = utt_net.cuda()
        line_net = line_net.cuda()

    lr = args.lr
    utt_optimizer = getattr(optim, args.optim)(utt_net.parameters(), lr=lr)
    utt_optim = optim.Adam(utt_net.parameters(), lr=lr)
    line_optimizer = getattr(optim, args.optim)(line_net.parameters(), lr=lr)
    line_optim = optim.Adam(line_net.parameters(), lr=lr)

    f1 = 0
    recall = 0
    predict = copy.deepcopy(input_test_label_org)
    for epoch in range(1, args.epochs + 1):
        Train(epoch)
        accuracy_f1, accuracy_recall, pre_label, true_label = Test(test_len)
        if epoch % 15 == 0:
            lr /= 10
            for param_group in utt_optimizer.param_groups:
                param_group['lr'] = lr
        if (accuracy_recall > recall):
            num = 0
            for x in range(len(predict)):
                predict[x] = pre_label[num]
                num = num + 1
            result_label = predict
            recall = accuracy_recall
        print("Best Result Until Now:")
        print(recall)

    onegroup_result = []
    for i in range(len(input_test_data_id)):
        a = {}
        a['id'] = input_test_data_id[i]
        a['Predict_label'] = predict[i]
        a['True_label'] = input_test_label_org[i]
        onegroup_result.append(a)
    Final_result.append(onegroup_result)
    Fineal_f1.append(recall)

true_label = []
predict_label = []

for i in range(len(Final_result)):
    for j in range(len(Final_result[i])):
        num = num + 1
        predict_label.append(Final_result[i][j]['Predict_label'])
        true_label.append(Final_result[i][j]['True_label'])
print(num)
accuracy_recall = recall_score(true_label, predict_label, average='macro')
accuracy_f1 = metrics.f1_score(true_label, predict_label, average='macro')
CM_test = confusion_matrix(true_label, predict_label)

print(accuracy_recall, accuracy_f1)
print(CM_test)

file = open('Final_result' + load_name + '.pickle', 'wb')
pickle.dump(Final_result,file)
file.close()
file = open('Final_f1'+ load_name +'.pickle', 'wb')
pickle.dump(Fineal_f1,file)
file.close()