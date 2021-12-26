#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：recommendSystem 
@File    ：main.py
@Author  ：hujinrun
@Date    ：2021/12/26 3:02 下午 
'''
import Experiment
# 随机试验
# # 1. random实验
# M, N = 8, 10
# K = 0 # 为保持一致而设置，随便填一个值
# random_exp = Experiment.Experiment(M, K, N, rt='Random')
# random_exp.run()

# # 2. MostPopular实验
# M, N = 8, 10
# K = 0 # 为保持一致而设置，随便填一个值
# mp_exp = Experiment.Experiment(M, K, N, rt='MostPopular')
# mp_exp.run()

# 3. UserCF实验
M, N = 8, 10
for K in [5, 10, 20, 40, 80, 160]:
    cf_exp =Experiment.Experiment(M, K, N, rt='UserCF')
    cf_exp.run()