import json
from enum import Enum
node_object = {
        "BOOLEAN": {"return_type": "BOOLEAN", "n_child": 0, "arg_type": [], "representation": "L", "values":{"choice": [0, 1]}, "min_depth": 1, "max_depth":1}, 
        "CLASS": {"return_type":"CLASS", "n_child":0, "arg_type":[],"representation":"L", "values":{"uniform_int":[0,9]}, "min_depth":1, "max_depth":1},
        "MODULE": {"return_type": "REAL", "n_child": 0, "arg_type": [], "representation": "L", "min_depth": 1, "max_depth":1}, 
    "LITERAL": {"return_type": "REAL", "n_child": 0, "arg_type": [], "representation": "L", "values":{"uniform_int": [0,783]}, "min_depth": 1, "max_depth":1},
    "REAL": {"return_type": "REAL", "n_child": 0, "arg_type": [], "representation": "L", "values": {"uniform_float": [-1.0, 1.0]}, "min_depth": 1, "max_depth":1},
    "LT": {"return_type": "BOOLEAN", "n_child": 2, "arg_type": ["REAL", "REAL"], "min_depth": 2},  
    "GT": {"return_type": "BOOLEAN", "n_child": 2, "arg_type": ["REAL", "REAL"], "min_depth": 2},
    "NOT": {"return_type": "BOOLEAN", "n_child": 1, "arg_type": ["BOOLEAN"], "min_depth": 3},
    "AND": {"return_type": "BOOLEAN", "n_child": 2, "arg_type": ["BOOLEAN", "BOOLEAN"], "min_depth": 3},
    "OR": {"return_type": "BOOLEAN", "n_child": 2, "arg_type": ["BOOLEAN", "BOOLEAN"], "min_depth": 3},
    "IFELSE": {"return_type": "REAL", "n_child": 3, "arg_type": ["REAL", "REAL", "BOOLEAN"], "representation": "IFELSE", "min_depth": 3},
    "IFELSE-CLS": {"return_type": "CLASS", "n_child": 3, "arg_type": ["CLASS", "CLASS", "BOOLEAN"], "representation": "IFELSE", "min_depth": 3},
    "ADD": {"return_type": "REAL", "n_child": 2, "arg_type": ["REAL", "REAL"], "min_depth": 2},  
    "SUB": {"return_type": "REAL", "n_child": 2, "arg_type": ["REAL", "REAL"], "min_depth": 2},
    "MUL": {"return_type": "REAL", "n_child": 2, "arg_type": ["REAL", "REAL"], "min_depth": 2},
    "MINUS": {"return_type": "REAL", "n_child": 1, "arg_type": ["REAL"], "min_depth": 2},
}

class NodeType(Enum):
    REAL=0
    BOOLEAN=1
    LITERAL=2
    CLASS=3
    string_to_node={
        "REAL":REAL,
        "BOOLEAN":BOOLEAN,
        "LITERAL":LITERAL,
        "CLASS":CLASS,
    }
    @staticmethod
    def get_node_candidates(node_type, depth, max_depth, min_depth, module_dict=None):
        l = []
        for k in node_object.keys():
            if k =='BOOLEAN': continue
            if k =='MODULE': continue
            if node_object[k]['return_type']==node_type :
                if node_object[k]['min_depth'] + depth <= max_depth:
                    #l.append(k)
                    if 'max_depth' in node_object[k].keys():
                        if node_object[k]['max_depth'] + depth >= min_depth:
                            l.append(k)
                    else:
                        l.append(k)
        
        if module_dict is not None and node_type == "REAL":
            l.append('MODULE')
        return l



