#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：util.py
@Author  ：hujinrun
@Date    ：2021/12/18 8:25 下午 
'''
import random
import math
from operator import  itemgetter

def SplitData(data, M, k, seed):
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
    for user, item in data:
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


def Recall(train, test, N, GetRecommendation):
    """
    :param train:
    :param test:
    :param N:
    :return:
    """
    hit = 0
    all = 0
    for user in train.keys():
        if user not in test:
            continue
        tu = test[user]
        rank = GetRecommendation(user, N)
        for item, pui in rank.items():
            if item in tu:
                hit += 1
        all += len(tu) # 用户喜欢的作品总数
    return hit/(all*1.0)

def Precision(train, test, N, GetRecommendation):
    """
        :param train:
        :param test:
        :param N:
        :return:
        """
    hit = 0
    all = 0
    for user in train.keys():
        if user not in test:
            continue
        tu = test[user]
        rank = GetRecommendation(user, N)
        for item, pui in rank.items():
            if item in tu:
                hit += 1
        all += N # 召回的作品总数
    return hit / (all * 1.0)

def Coverage(train, test, N, GetRecommendation):
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user]:
            all_items.add(item)
        rank = GetRecommendation(user, N)
        for item, pui in rank.items():
            recommend_items.add(item)
    return len(recommend_items)/(len(all_items)*1.0)

def Popularity(train, test, N, GetRecommendation):
    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            if item not in item_popularity:
                item_popularity[item]=0
            item_popularity[item] += 1
    ret = 0
    n = 0
    for user in train.keys():
        rank = GetRecommendation(user, N)
        for item, pui in rank.items():
            ret += math.log(1+item_popularity[item])
            n += 1
    ret /= n*1.0
    return ret

def UserSimilarity(train):
    W = dict()
    for u in train.keys():
        for v in train.keys():
            if u == v:
                continue
            W[u][v] = len(train[u]&train[v])
            W[u][v] /= math.sqrt(len(train[u])*len(train[v])*1.0)
    return W

def UserSimilarityWithInverseTable(train):
    # 构建倒排索引表
    item_users = dict()
    for u, items in train.items():
        for item in items:
            if item not in item_users:
                item_users[item] = []
            item_users[item].append(u)
    # 计算物品打分
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u in users:
            if u not in N:
                N[u] = 0
                C[u] = dict()
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1
    # 计算相似度
    W = dict()
    for u, related_users in C.items():
        if u not in W:
            W[u] = dict()
        for v, cuv in related_users.items():
            W[u][v] = cuv/math.sqrt(N[u]*N[v])
    return W

def Recommend(user, train, W, K):
    rank = dict()
    interacted_items = train[user]
    for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:K]:
        for i, rvi in train[v].items():
            if i in interacted_items:
                continue
            rank[i] += wuv*rvi
    return rank

def UserCF(train):
    """
    :params: train, 训练数据集
    :params: K, 可忽略
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
    N = dict()
    C = dict()
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
    def GetRecommendation(user,N):
        rank = dict()
        interacted_items = train[user]
        for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:N]:
            for i in train[v]:
                if i in interacted_items:
                    continue
                if i not in rank:
                    rank[i] = 0
                rank[i] += wuv
        return rank
    return GetRecommendation

def UserIIF(train):
    """
    :params: train, 训练数据集
    :params: K, 可忽略
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
    N = dict()
    C = dict()
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
                C[user][otheruser] += 1 / math.log(1+len(users))
    # 计算相似度
    W = dict()
    for user, otherusers in C.items():
        if user not in W:
            W[user] = dict()
        for otheruser, relative in otherusers.items():
            W[user][otheruser] = relative/math.sqrt(N[user]*N[otheruser])
    # 获取推荐结果
    def GetRecommendation(user,N):
        rank = dict()
        interacted_items = train[user]
        for v, wuv in sorted(W[user].items(), key=itemgetter(1), reverse=True)[0:N]:
            for i in train[v]:
                if i in interacted_items:
                    continue
                if i not in rank:
                    rank[i] = 0
                rank[i] += wuv
        return rank
    return GetRecommendation


