import numpy as np
import pandas as pd
from oedm.student_activity import settings
from oedm.student_activity import ActivityModel

# 用户指标
# data = np.array([
#     [0, 250, 1, 2, 1, 1, 0.3],
#     [2, 500, 2, 1, 4, 3, 0.7],
#     [3, 600, 1, 3, 1, 4, 0.8],
#     [3, 800, 1, 2, 1, 1, 0.4],
#     [5, 2000, 6, 7, 3, 8, 0.9],
#     [10, 4000, 8, 9, 7, 14, 0.9],
# ])
#
# # 上个月的积极度
# last_activity = [380, 470, 610, 750, 450, 700]
#
# # 计算积极度
# modle = ActivityModel()
# activity, add_list = modle.calc_activity(data, last_activity, get_add_list=True)
#
# # 输出计算结果
# print(activity)
# print(add_list)

# data = pd.read_csv('test_data/data1.csv', header=0)
#
# modle = ActivityModel()
# modle.run_model(data, out_type='csv')



