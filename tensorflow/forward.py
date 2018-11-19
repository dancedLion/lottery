import tensorflow as tf
import numpy as np


'''
计算概率
影响因素:
1-每一次的初始化概率
2-数的距离
3-相互数的概率
    4-数的顺序

'''

fl=[i+1 for i in range(35)]
bl=[i+1 for i in range(15)]

