import time

import torch
from  torchvision.datasets import MNIST
from torchvision import transforms
import torch.nn as nn
from torch.autograd import Variable
import numpy as np


from nn_model import *
from tree import *

dataset = MNIST(root='./mnist/',transform=transforms.Compose([transforms.ToTensor()]))


train_loader = torch.utils.data.DataLoader(
            dataset,
            batch_size = 128, 
            shuffle=True
        )


def tree_to_nn(tree, net, optimizer):
    loss_function = nn.MSELoss()
    mean_loss=[]
    for i in range(1):
        epoch_time = time.time()
        for (data, target) in train_loader:


            data_var = Variable(data,volatile=True).cuda()
            y = t.evaluate(data_var).data
            y_var = Variable(y).cuda()

            data_var = Variable(data).cuda()
            y_pred = net(data_var)

            loss = loss_function(y_pred,y_var)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            mean_loss.append(loss.cpu().data[0])
        if np.mean(mean_loss)<0.01:
            break
    return np.mean(mean_loss)


t = Tree(root_type='CLASS')
print(t)
print(t.get_fitness(data_loader=train_loader))
print(t.get_fitness(data_loader=train_loader))
