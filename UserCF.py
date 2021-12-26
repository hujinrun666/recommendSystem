#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：Algorithm.py
@Author  ：hujinrun
@Date    ：2021/12/26 2:42 下午 
'''
import math
from operator import  itemgetter
def UserCF(train, K, Nitem):
    """
    :params: train, 训练数据集
    :params: K topK的用户数
    :params: N, 超参数，设置取TopN推荐物品数目
    :return: GetRecommendation, 推荐接口函数
    """
    # 1.构建倒排
    # 2.计算召回和正样本的数量
    # 3.计算打分
    # train : user->items
    itemToUser = dict()
    for user, items in train.items():
        for item in items:
            if item not in itemToUser:
                itemToUser[item] = set()
            itemToUser[item].add(user)
    # 找到用户u存在正反馈的物品数据和用户v存在正反馈的物品数量，以及用户u，v共同存在正反馈的物品数量
    N = dict() # 统计每个用户消费过的作品数
    C = dict() # 统计两个用户共同消费过的作品数
    for item,users in itemToUser.items():
        for user in users:
            if user not in (N,C):
                N[user] = 0
                C[user] = dict()
            N[user] += 1
            for otheruser in users:
                if user == otheruser:
                    continue
                if otheruser not in C[user]:
                    C[user][otheruser] = 0
                C[user][otheruser] += 1
    # 计算相似度
    W = dict()
    for user, otherusers in C.items():
        if user not in W:
            W[user] = dict()
        for otheruser, relative in otherusers.items():
            W[user][otheruser] = relative/math.sqrt(N[user]*N[otheruser])
    # 获取推荐结果
    def GetRecommendation(user):
        rank = dict()
        interacted_items = train[user]
        # 选出相似度最高的K个用户
        for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for i in train[v]:
                if i in interacted_items:
                    continue
                if i not in rank:
                    rank[i] = 0
                rank[i] += wuv
        recs = list(sorted(rank.items(), key=lambda x: x[1], reverse=True))[:Nitem]
        return recs
    return GetRecommendation