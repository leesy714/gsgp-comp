
import pandas as pd
import numpy as np

import graphviz

from gp import *

def init_gp(evaluator, max_depth=8, pop_size=100):
    initial = RampedHalfAndHalf()
    selection = RandomSelection()
    replacement = ElitismPreselection()
    mutation = SubtreeMutation()
    crossover = SubtreeCrossover()
    fitness = GainPlusLogMatchFitness(evaluator, 0.05 , 8, 1.0)
    gp = GP(pop_size, evaluator, selection, replacement, initial, mutation, crossover, fitness)
    return gp

def switch_target(evaluator, target):
    if target is 'train':
        evaluator.set_data_type(EvalDataType.train)
    elif target is 'validation':

        evaluator.set_data_type(EvalDataType.validation)
    else:
        evaluator.set_data_type(EvalDataType.test)
    return


class GpuEval(object):
    def __init__(self, day=20, start_gpu_num=0, n_gpu=4, data_txt=None):
        if data_txt:
            self.evaluator = GPUEvaluator(data_txt, "match_result.txt", "./stockdata.dump", "./hostdata.dump", day, False, True, EvalDataType.train, n_gpu, start_gpu_num)
        else:
            self.evaluator = GPUEvaluator("match_result.txt", "./stockdata.dump", "./hostdata.dump", day, False, True, EvalDataType.train, n_gpu, start_gpu_num)
            
    def __del__(self):
        del self.evaluator

    def eval_text(self, pattern, target='train', fitness=None):
        switch_target(self.evaluator, target)
        t = Tree(pattern.rstrip())
        if fitness is None:
            fitness = ArithGeomFitness(500, 8)
        ev = self.evaluator.evaluate(t)
        offspring = Individual(t, ev)
        fit = fitness.get_fitness(offspring);
        ev.fitness = fit;
        return ev;

    def get_match_result(self, pattern):
        self.evaluator.deliver_match_result(True)
        ev = self.eval_text(pattern)
        mr = ev.match_result
        self.evaluator.deliver_match_result(False)
        match_result = np.array(mr.match_result, dtype=np.float)
        stk_cd = np.array(mr.stk_cd,dtype=np.int)
        ymd = np.array(mr.ymd, dtype=np.int)
        return match_result, stk_cd, ymd


if __name__=='__main__':
    gpu_eval = GpuEval()
    train_result=gpu_eval.eval_text('SHIFT -1 CPRC 0 SHIFT -1 CPRC 0 EQ 0', target='train')
    print(train_result)

    match_result, match_ymd = gpu_eval.get_match_result('SHIFT -1 CPRC 0 SHIFT -1 CPRC 0 EQ 0')
    print(match_result[:10])
    print(match_ymd[:10])
