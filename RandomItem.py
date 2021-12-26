#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：RandomItem.py
@Author  ：hujinrun
@Date    ：2021/12/26 2:54 下午 
'''
import random
# 1. 随机推荐
def Random(train, K, N):
    '''
    :params: train, 训练数据集
    :params: K, 可忽略
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation，推荐接口函数
    '''
    items = {}
    for user in train:
        for item in train[user]:
            items[item] = 1

    def GetRecommendation(user):
        # 随机推荐N个未见过的
        user_items = set(train[user])
        # 筛选出在不在用户列表中得作品
        rec_items = {k: items[k] for k in items if k not in user_items}
        rec_items = list(rec_items.items())
        random.shuffle(rec_items)
        return rec_items[:N]
    return GetRecommendation