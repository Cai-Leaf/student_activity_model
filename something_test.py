import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from oedm.student_activity import ActivityModel
import logging
import time
import datetime

# a = np.array([[0, 1, 2, 3],
#                [3, 4, 5, 4],
#                [6, 7, 8, 8]])
# print(a.shape)

#
# b = np.array([[1, 2, 3],
#                [1, 2, 3],
#                [1, 2, 3]])
# # c = pd.DataFrame(a, index=['1', '2', '3'], columns=['A', 'B', 'C'])
# #
# # print(c[(c['A'] > 2) & (c['B'] > 4)])
#
#
#
#
# print((y ** 5))

# x = np.array(range(1, 21)).astype(np.float64)
# y = np.array([4, 11, 41, 91, 151, 251, 500, 1001, 2001, 5001, 10001, 20001, 50001, 100001, 200001, 500001, 10000001, 20000001, 50000001, 100000001]).astype(np.float64)
# z1 = np.polyfit(x, y, 4)#用3次多项式拟合
# p1 = np.poly1d(z1)
# print(p1) #在屏幕上打印拟合多项式
# yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
# plot1 = plt.plot(x, y, '*', label='original values')
# plot2 = plt.plot(x, yvals, 'r', label='polyfit values')
# plt.xlabel('x axis')
# plt.ylabel('y axis')
# plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
# plt.title('polyfitting')
# plt.show()

# start = time.time()
# model = ActivityModel()
# model.run_model('test_data_oct/data_big.csv', 'test_data_oct/data_big_addlist.csv')
# print('运行了'+str(time.time()-start)+"秒")

#
# def calc_func(x):
#     result = 0.5*(900-x)-25
#     return result if result > 1 else 1
#
# start = 450
# score_list = [450]
# for i in range(30):
#     start = np.round(start + calc_func(start))
#     score_list.append(start)
#     print(i, start)
#
#
# plot1 = plt.plot(range(len(score_list)), score_list, 'r', label='polyfit values')
# plt.xticks(range(len(score_list)))
# plt.show()

# 用户指标
# data = np.array([
#     ['清华大学', 0, 250, 1, 2, 1, 1, 0.3],
#     ['清华大学', 2, 500, 2, 1, 4, 3, 0.7],
#     ['北京大学', 3, 600, 1, 3, 1, 4, 0.8],
#     ['清华大学', 3, 800, 1, 2, 1, 1, 0.4],
#     ['对外经济贸易大学', 5, 2000, 6, 7, 3, 8, 0.9],
#     ['清华大学', 7, 4000, 8, 9, 7, 14, 0.9],
# ])
#
# data2 = np.array([
#     [0, 250, 1],
#     [2, 500, 2],
#     [3, 600, 1],
#     [3, 800, 1],
#     [5, 2000, 6],
#     [7, 4000, 8],
# ])
#
# data4 = np.array([
#     [6, 250, 1],
#     [6, 500, 2],
#     [6, 600, 1],
#     [6, 800, 1],
#     [6, 2000, 6],
#     [6, 4000, 8],
# ])
#
# data3 = np.array([
#     [0, 0, 1, 'a'],
#     [2, 500, 2, 'a'],
#     [3, 600, 1, 'b'],
#     [3, 800, 1, 'b'],
#     [5, 2000, 6, 'c'],
#     [7, 4000, 8, 'c'],
# ])
#
# # 上个月的积极度
# last_activity = [380, 470, 610, 750, 450, 700]

# 计算积极度
modle = ActivityModel()
modle.run_model('test_data/data1.csv', int_type='csv', out_type='db')
# activity, add_list = modle.calc_activity(data, last_activity, get_add_list=True)
#[ 428.  486.  592.  596.  596.  774.]
# 输出计算结果
# print(activity)
# print(add_list)

# test = pd.DataFrame(data2, columns=['A', 'B', 'C'])
# test['D'] = test['B'].values / test['A'].values
# test.fillna(value=0)
# print(test)
# index = test[-test['D'].isin(['a'])].index
#
# print(test.loc[index][['A', 'B']])
# print(np.column_stack((data2, data4)))