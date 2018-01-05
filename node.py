import torch
from utils.node_util import *
import numpy as np


class Node(object):
    def __init__(self, nid, node_name=None, recursive=False, depth=0, module_dict=None):
        self.nid=nid
        self.node_name = node_name
        self.node_info = node_object[self.node_name]
        self.depth = depth
        self.module_dict = module_dict

        self.child=[]
        if self.node_name == 'MODULE':
            if self.module_dict is None:
                raise ValueError
            self.value=np.random.randint(0,len(module_dict))
        else:
            if "values" in self.node_info.keys():
                if "choice" in self.node_info['values'].keys():
                    candidate = self.node_info['values']['choice']
                    self.value=np.random.choice(candidate)
                elif "uniform_int" in self.node_info['values'].keys():
                    low = self.node_info['values']['uniform_int'][0]
                    high = self.node_info['values']['uniform_int'][1]+1
                    candidate = range(low, high)
                    self.value=np.random.choice(candidate)
                else:
                    low = self.node_info['values']['uniform_float'][0]
                    high = self.node_info['values']['uniform_float'][1]
                    self.value = np.random.rand()*(high-low)+low
    
            else:
                self.value = None
        if recursive:
            for ch in self.node_info['arg_type']:
                self.child.append(NodeGenerator.generate(node_type=ch, recursive=recursive, depth=self.depth, module_dict=module_dict))


    def __repr__(self):
        if self.value is not None:
            my_repr = '{} {:.2f}'.format(self.node_name,self.value)
        else:
            my_repr = '{}'.format(self.node_name)


        if len(self.child)==0:
            return my_repr
        s = ''
        for ch in self.child:
            s = s + str(ch) +' '
        s = s+my_repr
        return s 

    def get_max_depth(self):
        if len(self.child)==0:
            return self.depth
        max_depth=self.depth
        for ch in self.child:
            ch_depth = ch.get_max_depth()
            if ch_depth > max_depth:
                max_depth = ch_depth
        return max_depth

    def get_node_count(self):
        if len(self.child)==0:
            return 1
        a = 1
        for ch in self.child:
            ch_count = ch.get_node_count()
            a+=ch_count
        return a
        
    def forward(self, data):
        if self.node_name in ['REAL', 'BOOLEAN','CLASS']:
            return self.value
        elif self.node_name == 'LITERAL':
            x = int(self.value) // 28
            y = int(self.value) % 28
            return data[:,:,x,y]
        elif self.node_name == 'NOT':
            v1 = self.child[0].forward(data)
            return 1 - v1
        elif self.node_name == 'MINUS':
            v1 = self.child[0].forward(data)
            return -v1
        elif self.node_name == 'MODULE':
            v1 = self.module_dict[self.value](data)

            return v1

        v1 = self.child[0].forward(data)
        v2 = self.child[1].forward(data)

        if self.node_name == 'LT':
            if type(v1) is float and type(v2) is float:
                return float(v1<v2)
            return (v1<v2).float()
        elif self.node_name == 'GT':
            if type(v1) is float and type(v2) is float:
                return float(v1>v2)

            return (v1>v2).float()

        elif self.node_name == 'AND':
            return v1 * v2
        elif self.node_name == 'OR':

            return 1 - (1 - v1) * (1 - v2)
        elif self.node_name == 'ADD':

            return v1 + v2
        elif self.node_name == 'SUB':

            return v1 - v2
        elif self.node_name == 'MUL':
            return v1 * v2
        elif self.node_name == 'IFELSE':
            v3 = self.child[2].forward(data)

            return v3 * v1 + (1 - v3) * v2
        elif self.node_name == 'IFELSE-CLS':
            v3 = self.child[2].forward(data)
            return v1 * v3 + v2 * (1 - v3)


















 







class NodeGenerator(object):
    max_depth=4
    min_depth=3
    @staticmethod
    def generate(node_name=None,node_type=None, recursive=True, depth=0, module_dict=None):
        if node_name is None:
            l = NodeType.get_node_candidates(node_type, depth, NodeGenerator.max_depth, NodeGenerator.min_depth, module_dict=module_dict)
            node_name=np.random.choice(l)
        return Node(0,node_name=node_name, recursive=recursive,depth=depth+1, module_dict=module_dict)


if __name__ == '__main__':
    n = NodeGenerator.generate(node_type='BOOLEAN')
    print(n)
