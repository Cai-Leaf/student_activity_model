from oedm.student_activity import ActivityModel
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def draw_bar(labels, quants, other):
    width = 0.5
    ind = np.linspace(0.5, len(quants)-0.5, len(quants))
    # make a square figure
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    # Bar Plot
    ax.bar(ind, quants, width, color='blue', edgecolor='black')
    # 柱子上加字
    for i in range(len(quants)):
        plt.text(ind[i], quants[i] + np.max(quants) / 100, str(quants[i])+" ("+str(other[i])+"%)", ha='center')
    # Set the ticks on x-axis
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    # labels
    ax.set_xlabel('Interval')
    ax.set_ylabel('Number')
    # title
    plt.show()

data = pd.read_csv("test_data_oct/data_process_result.csv", header=0, index_col=0, encoding='utf-8')
data = data[['DT_MONTH', 'LOG_NUM', 'LOG_DURATION', 'LOG_DAY', 'CLICK_COURSE', 'T_F', 'C_PV', 'COMPLETION_WORK']]



# 数据按月份分隔
month_datas = [data[data.DT_MONTH == '2017-03-01'].sort_index(),
               data[data.DT_MONTH == '2017-04-01'].sort_index(),
               data[data.DT_MONTH == '2017-05-01'].sort_index(),
               data[data.DT_MONTH == '2017-06-01'].sort_index(),
               data[data.DT_MONTH == '2017-07-01'].sort_index(),
               data[data.DT_MONTH == '2017-08-01'].sort_index()]
month_datas = [month_data.drop(['DT_MONTH'], axis=1) for month_data in month_datas]
for month_data in month_datas:
    print(len(month_data[(month_data['LOG_NUM'] >= 6) & (month_data['LOG_DURATION'] >= 3600)]))
#
#
# # 计算积极度
# activity_score = [450]*len(month_datas[0])
# max_score = [450]
# modle = ActivityModel()
# month_num = 0
# month = 54
# for i in range(month):
#     activity_score = modle.calc_activity(month_datas[month_num], activity_score)
#     max_score.append(np.max(activity_score))
#     if month_num < len(month_datas)-1:
#         month_num += 1
#     else:
#         month_num = 0
#
# # 输出积极度区间及比例
# max_value = np.max(activity_score)
# print(max_value)
# min_value = 350
# # interval = [min_value+i*(max_value-min_value)/5 for i in range(6)]
# interval = [350, 450, 500, 600, 900]
# print(interval)
# ratio = [0]*(len(interval)-1)
# for num in activity_score:
#     for i in range(len(ratio)):
#         if num >= interval[i] and num < interval[i+1]:
#             ratio[i] += 1
# print(np.array(ratio))
# print(np.array(ratio)/len(activity_score)*100)
# # 画图
# # labels = [str(interval[i])+'-'+str(interval[i+1]) for i in range(len(interval)-1)]
# # draw_bar(labels, ratio, np.round(np.array(ratio)/len(activity_score)*100, 2))
#
# # fig1, ax1 = plt.subplots()
# # ax1.scatter(range(len(activity_score)), sorted(activity_score, reverse=True))
# # plt.show()
#
# # 展示最大值的积极度变化情况
# fig1, ax1 = plt.subplots()
# ax1.scatter(range(len(max_score)), max_score)
# # fig2, ax2 = plt.subplots()
# # ax2.scatter(range(len(activity_score)), np.sort(activity_score, kind='quicksort'))
# plt.show()

# zero_num = 0
# for i in activity_score:
#     if i == 350:
#         zero_num += 1
# print(zero_num)

# 月活跃度数据展示
# activity_score = [450]*len(month_datas[month-1])
# modle = ActivityModel()
# activity_score, add_list = modle.calc_activity(month_datas[month-1], activity_score, get_add_list=True)
# month_activity_score = add_list[:, 7]
# max_value = 1
# min_value = 0
# interval = [0, 0.25, 0.5, 0.75, 1]
# ratio = [0]*(len(interval)-1)
# for num in month_activity_score:
#     for i in range(len(ratio)):
#         if num >= interval[i] and num < interval[i+1]:
#             ratio[i] += 1
# print(np.array(ratio))
# print(np.array(ratio)/len(month_activity_score)*100)
# labels = [str(interval[i])+'-'+str(interval[i+1]) for i in range(len(interval)-1)]
# draw_bar(labels, ratio, np.round(np.array(ratio)/len(activity_score)*100, 2))


