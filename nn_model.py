import torch
import torch.nn as nn
import torch.nn.functional as F


class MLPClassifier(nn.Module):
    def __init__(self, input_size, hiddens=(128,), activation=F.relu):
        super(MLPClassifier, self).__init__()
        self.hiddens=hiddens
        self.activation = activation
        self.module_list = nn.ModuleList()
        last_node = input_size
        for l in hiddens:

            self.module_list.append(nn.Linear(last_node, l))
            last_node = l
        self.head = nn.Linear(last_node, 2)

    def forward(self, x):
        x = x.view(x.size(0),-1)
        for module in self.module_list:
            x = self.activation(module(x))
        x = self.head(x)
        return x



class MLPRegressor(nn.Module):
    def __init__(self, input_size, hiddens=(128,), activation=F.relu):

        super(MLPRegressor, self).__init__()
        self.hiddens=hiddens
        self.activation = activation
        self.module_list = nn.ModuleList()
        last_node = input_size
        for l in hiddens:
            self.module_list.append(nn.Linear(last_node, l))
            last_node = l
        self.head = nn.Linear(last_node, 1)

    def forward(self, x):
        x = x.view(x.size(0),-1)
        for module in self.module_list:
            x = self.activation(module(x))
        x = self.head(x)
        return x




