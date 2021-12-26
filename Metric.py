#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：Metric.py
@Author  ：hujinrun
@Date    ：2021/12/19 1:05 上午 
'''
import math

class Metric():
    """
    对召回效果测量的类
    train-训练集
    test-测试集
    GetRecommendation - 获取召回结果的函数
    """
    def __init__(self, train, test, GetRecommendation):
        self.train = train
        self.test = test
        self.GetRecommendation = GetRecommendation

    def Recall(self):
        """
        计算召回率
        :param train:
        :param test:
        :param N:
        :return:
        """
        hit = 0
        all = 0
        for user in self.train.keys():
            if user not in self.test:
                continue
            tu = self.test[user]
            rank = self.GetRecommendation(user)
            for item, pui in rank:
                if item in tu:
                    hit += 1
            all += len(tu)  # 用户喜欢的作品总数
        return round(hit / (all * 1.0)*100, 2)

    def Precision(self):
        """
            :param train:
            :param test:
            :param N:
            :return:
            """
        hit = 0
        all = 0
        for user in self.train.keys():
            if user not in self.test:
                continue
            tu = self.test[user]
            rank = self.GetRecommendation(user)
            for item, pui in rank:
                if item in tu:
                    hit += 1
            all += len(rank)  # 召回的作品总数
        return round(hit / (all * 1.0)*100,2)

    def Coverage(self):
        recommend_items = set()
        all_items = set()
        for user in self.train.keys():
            for item in self.train[user]:
                all_items.add(item)
            rank = self.GetRecommendation(user)
            for item, pui in rank:
                recommend_items.add(item)
        return round((len(recommend_items) / (len(all_items) * 1.0))*100, 2)

    def Popularity(self):
        item_popularity = dict()
        for user, items in self.train.items():
            for item in items:
                if item not in item_popularity:
                    item_popularity[item] = 0
                item_popularity[item] += 1
        ret = 0
        n = 0
        for user in self.train.keys():
            rank = self.GetRecommendation(user)
            for item, pui in rank:
                ret += math.log(1 + item_popularity[item])
                n += 1
        ret /= n * 1.0
        return round(ret, 4)

    def eval(self):
        metric = {'Precision': self.Precision(),
                  'Recall': self.Recall(),
                  'Coverage': self.Coverage(),
                  'Popularity': self.Popularity()}
        print('Metric:', metric)
        return metric