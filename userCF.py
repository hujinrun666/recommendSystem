#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：userCF.py
@Author  ：hujinrun
@Date    ：2021/12/18 9:11 下午 
'''
import util
datas = []
count = 0
with open("./data/u.data") as lines:
    for line in lines:
        line = line.replace('\n','')
        splitedLine = line.split("\t")[0:2]
        datas.append(splitedLine)
        count += 1
train, test = util.SplitData(datas, 10, 1, 10)
getRecommendation = util.UserIIF(train)
print("recall",util.Recall(train, test, 80, getRecommendation))
print("Precision", util.Precision(train, test, 80, getRecommendation))
print("Coverage", util.Coverage(train, test, 80, getRecommendation))
print("Popularity", util.Popularity(train, test, 80, getRecommendation))

# print(train)
# print(test)
