#!/usr/bin/env python
# -*- coding: unicode_escape -*-
'''
@Project ：recommendSystem 
@File    ：Dataload.py
@Author  ：hujinrun
@Date    ：2021/12/19 1:04 上午 
'''
import random
import common
class DataSet():
    def __init__(self, fp):
        self.data = self.loadData(fp)

    @common.timmer
    def loadData(self, fp):
        data = []
        with open(fp, encoding="unicode_escape") as lines:
            for l in lines:
                # 将各个元素都转换成int类型
               data.append(tuple(map(int, l.strip().split('::')[:2])))
            return data

    def splitData(self, M, k, seed=1):
        """
        :param data: 数据集
        :param M: 数据分成的数量
        :param k: 随机数
        :param seed: 随机种子
        :return: 训练集和测试集
        """
        test = []
        train = []
        random.seed(seed)
        for user, item in self.data:
            if random.randint(0, M) == k:
                test.append([user, item])
            else:
                train.append([user, item])

        def convToDic(innerdata):
            dicdata = dict()
            for user, item in innerdata:
                if user not in dicdata:
                    dicdata[user] = set()
                dicdata[user].add(item)
            return dicdata
        return convToDic(train), convToDic(test)

