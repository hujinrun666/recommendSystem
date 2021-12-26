#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：Experiment.py
@Author  ：hujinrun
@Date    ：2021/12/25 9:29 下午 
'''
import Metric
import common
import Dataload
import RandomItem
import UserCF
import UserIIF
import MostPopular

class Experiment():
    def __init__(self, M, K, N, fp = "./data/ratings.dat", rt = "Random"):
        """
        :params: M, 进行多少次实验
        :params: K, TopK相似用户的个数
        :params: N, TopN推荐物品的个数
        :params: fp, 数据文件路径
        :params: rt, 推荐算法类型
        """
        self.M = M
        self.K = K
        self.N = N
        self.fp = fp
        self.rt = rt
        self.alg = {'Random': RandomItem.Random, 'MostPopular': MostPopular.MostPopular, \
                    'UserCF': UserCF.UserCF, 'UserIIF': UserIIF.UserIIF}

    # 定义单次实验
    @common.timmer
    def worker(self, train, test):
        '''
        :params: train, 训练数据集
        :params: test, 测试数据集
        :return: 各指标的值
        '''
        getRecommendation = self.alg[self.rt](train, self.K, self.N)
        metric = Metric.Metric(train, test, getRecommendation)
        return metric.eval()

    # 多次实验取平均
    @common.timmer
    def run(self):
        metrics = {'Precision': 0, 'Recall': 0,
                   'Coverage': 0, 'Popularity': 0}
        dataset = Dataload.DataSet(self.fp)
        for ii in range(self.M):
            train, test = dataset.splitData(self.M, ii)
            print('Experiment {}:'.format(ii))
            metric = self.worker(train, test)
            metrics = {k: metrics[k] + metric[k] for k in metrics}
        metrics = {k: metrics[k] / self.M for k in metrics}
        print('Average Result (M={}, K={}, N={}): {}'.format( \
            self.M, self.K, self.N, metrics))