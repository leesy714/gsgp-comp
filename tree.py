import numpy as np
from node import Node, NodeGenerator
import torch
from torch.autograd import Variable
class Tree(object):
    def __init__(self,root=None, root_type='BOOLEAN', module_dict=None):
        if root is None:
            self.root = NodeGenerator.generate(node_type=root_type, module_dict=module_dict)
        else:
            self.root = root
        self.fitness = None

    def evaluate(self, data):
        ret = self.root.forward(data)
        if type(ret) is float:
            ret = Variable( torch.zeros((data.size(0),))+ret)
        #ret = torch.tanh(ret)
        return ret

    def hamming_distance(self, data, y):
        y_pred = self.evaluate(data).squeeze().long()
        hamming_dist = torch.eq(y,y_pred).sum()
        return hamming_dist

    def get_fitness(self, data_loader=None):
        if self.fitness:
            return self.fitness
        else:
            distance = 0
            for x, y in data_loader:
                distance += self.hamming_distance(x,y)
            self.fitness = distance
            return self.fitness

        


    def __repr__(self):
        return str(self.root)
    
    def get_max_depth(self):
        return self.root.get_max_depth()
    def __len__(self):
        return self.root.get_node_count()


        

if __name__ =='__main__':
    t = Tree()
    print(t)

