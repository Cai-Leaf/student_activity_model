from oedm.student_activity import ActivityModel
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data = pd.read_csv("test_data/data_process_result.csv", header=0, index_col=0, encoding='utf-8')
data['LOG_DURATION'] = data['LOG_DURATION'].values*60

# 数据按月份分隔
month_datas = [data[data.DT_MONTH == '2017-03-01'],
               data[data.DT_MONTH == '2017-04-01'],
               data[data.DT_MONTH == '2017-05-01'],
               data[data.DT_MONTH == '2017-06-01'],
               data[data.DT_MONTH == '2017-07-01']]
month_datas = [month_data.drop(['DT_MONTH'], axis=1) for month_data in month_datas]

# 取所有学生的并集 使每份数据中学生的学号一致
stu_code = month_datas[0].index.tolist()
for i in range(1, len(month_datas)):
    stu_code = [code for code in stu_code if code in month_datas[i].index.tolist()]
month_datas = [month_data.loc[stu_code] for month_data in month_datas]

# 计算积极度
activity_score = [450]*len(month_datas[0])
max_score = [450]
modle = ActivityModel()
month_num = 0
for i in range(24):
    activity_score = modle.calc_activity(month_datas[month_num], activity_score)
    max_score.append(np.max(activity_score))
    if month_num < len(month_datas)-1:
        month_num += 1
    else:
        month_num = 0

# 输出积极度区间及比例
max_value = np.max(activity_score)
min_value = 350
interval = [min_value+i*(max_value-min_value)/5 for i in range(6)]
print(interval)
ratio = [0]*5
for num in activity_score:
    for i in range(len(ratio)):
        if num >= interval[i] and num < interval[i+1]:
            ratio[i] += 1
print(np.array(ratio))
print(np.array(ratio)/len(activity_score)*100)
# 展示最大值的积极度变化情况
# fig1, ax1 = plt.subplots()
# ax1.scatter(range(len(max_score)), max_score)
# # fig2, ax2 = plt.subplots()
# # ax2.scatter(range(len(activity_score)), np.sort(activity_score, kind='quicksort'))
# plt.show()

zero_num = 0
for i in activity_score:
    if i == 450:
        zero_num += 1
print(zero_num)




