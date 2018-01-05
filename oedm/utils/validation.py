"""
用于验证输入是否合法的一些函数
"""

import numpy as np


def check_array(array, feature_num=None, ensure_2d=True):
    array = np.array(array)
    if ensure_2d:
        if np.ndim(array) > 2 or np.ndim(array) < 1:
            raise ValueError("数组维度错误，接受的最高维度为2，您的数组维度为"+str(np.ndim(array)))
        if np.ndim(array) == 1:
            array = np.array([array])
        if np.shape(array)[-1] != feature_num:
            raise ValueError("特征数错误，接受的特征数为"+str(feature_num)+"，您的特征数为"+str(np.shape(array)[-1]))
    else:
        if np.ndim(array) > 1:
            raise ValueError("数组维度错误，接受的最高维度为1，您的数组维度为"+str(np.ndim(array)))
    return array


def check_dataframe(data, contain):
    try:
        data = data[contain]
    except KeyError:
        raise ValueError('输入的参数有误，未包含指定字段')
    return data


def check_matching(x, y):
    if len(x) != len(y):
        raise ValueError("输入参数的长度不匹配")
    return