from .settings import *
from ..utils.validation import check_array, check_matching, check_dataframe
from ..utils.file_process import read_csv_to_dataframe, make_dataframe_to_csv
from ..utils.time_process import get_last_month_date
from ..utils.db_process import mk_dataframe_and_save_to_db
import numpy as np
import pandas as pd


class ActivityModel:
    """在线教育学生积极度模型
        此模型可计算学生积极度，配置文件在相同目录下的settings.py中

        参数：
        ----------
        无

        属性：
        ----------
        TARGET_NAME : array
            指标名称数组，从配置文件读入
        TARGET_MIN_VAL : array
            指标的最小值数组，从配置文件读入
        TARGET_MAX_VAL : array
            指标的最大值数组，从配置文件读入
        TARGET_WEIGHT : array
            指标的权重分数组，从配置文件读入
        MAX_MONTH_ACTIVITY : int
            月活跃分最大值，为各指标权重分的总和，从配置文件读入
        TARGET_NUM : int
            指标权重的个数，从配置文件读入
        SPECIAL_TARGET_NAME : array
            特殊指标名称数组，从配置文件读入
        SPECIAL_TARGET_MIN_VAL : array
            特殊指标的最小值数组，从配置文件读入
        SPECIAL_TARGET_MAX_VAL : array
            特殊指标的最大值数组，从配置文件读入
        SPECIAL_TARGET_WEIGHT : array
            特殊指标的权重分数组，从配置文件读入
        SPECIAL_MAX_MONTH_ACTIVITY : int
            特殊月活跃分最大值，为各指标权重分的总和，从配置文件读入
        SPECIAL_TARGET_NUM : int
            特殊指标权重的个数，从配置文件读入

        作者：
        ----------
        蔡承烨，Tel:18817878160，E-mail：caichengye16@otcaix.iscas.ac.cn
        """

    def __init__(self):
        # 普通指标
        self.TARGET_NAME = [target['NAME'] for target in TARGET_WEIGHT_RANGE]
        self.TARGET_MIN_VAL = np.array([target['MIN_VAL'] for target in TARGET_WEIGHT_RANGE])
        self.TARGET_MAX_VAL = np.array([target['MAX_VAL'] for target in TARGET_WEIGHT_RANGE])
        self.TARGET_WEIGHT = np.array([target['WEIGHT'] for target in TARGET_WEIGHT_RANGE])
        self.MAX_MONTH_ACTIVITY = np.sum(self.TARGET_WEIGHT)
        self.TARGET_NUM = len(TARGET_WEIGHT_RANGE)
        # 特殊指标
        self.SPECIAL_TARGET_NAME = [target['NAME'] for target in SPECIAL_TARGET_WEIGHT_RANGE]
        self.SPECIAL_TARGET_MIN_VAL = np.array([target['MIN_VAL'] for target in SPECIAL_TARGET_WEIGHT_RANGE])
        self.SPECIAL_TARGET_MAX_VAL = np.array([target['MAX_VAL'] for target in SPECIAL_TARGET_WEIGHT_RANGE])
        self.SPECIAL_TARGET_WEIGHT = np.array([target['WEIGHT'] for target in SPECIAL_TARGET_WEIGHT_RANGE])
        self.SPECIAL_MAX_MONTH_ACTIVITY = np.sum(self.SPECIAL_TARGET_WEIGHT)
        self.SPECIAL_TARGET_NUM = len(SPECIAL_TARGET_WEIGHT_RANGE)

    def run_model(self, data, set_month=None, int_type='dataframe', out_type='csv'):
        """积极度模型运行函数
            参数：
            ----------
            data: pd.DataFrame or string
                学生信息
            set_month: string
                需要设置的月份，若为None则自动生成上月的年月值，如2017-09
            int_type: string
                输入数据的形式
                若为'dataframe'，则输入的data为pd.DataFrame
                若为'csv'，则输入的data为文件名，输入数据从csv文件中读取
            out_type: string
                输出数据的形式
                若为'db'，则数据写入到数据库中
                若为'csv'，则数据输出到积极度模型中间表文件csv文件中

            返回值：
            ----------
            1.积极度模型输出表文件 activity_out_before.csv
            2.当out_type为'db'时，数据写入到数据库
              当out_type为'csv'时，数据输出到积极度模型中间表文件csv文件 如add_list_out_2017-09.csv

        """

        # 读取数据
        if int_type == 'csv':
            data = read_csv_to_dataframe(data, contain=INPUT_DATA_CONTAIN)
        else:
            data = check_dataframe(data, contain=INPUT_DATA_CONTAIN)
        last_activity_data = read_csv_to_dataframe(INPUT_FILE_NAME, contain=INPUT_ADD_LIST_FILE_CONTAIN)

        # 修改列名
        last_activity_data.rename(columns={NAME['积极度分值']: NAME['上月积极度值']}, inplace=True)
        # 将有效作业数和已完成作业数处理成作业完成度
        data[NAME['作业完成度']] = data[NAME['已完成作业数']].values / (data[NAME['有效作业数']].values+0.000000001)
        # 按学号补全相应学生的上月积极度值
        data = pd.merge(data, last_activity_data, on=NAME['学生编号'], how='left')
        data = data.fillna({NAME['上月积极度值']: DEFAULT_SCORE})

        # 计算积极度
        activity, add_list = self.calc_activity(data[[NAME['高校名称']]+self.TARGET_NAME].values,
                                                data[NAME['上月积极度值']].values, get_add_list=True)

        # 处理月份
        if set_month is None:
            set_month = get_last_month_date()

        # 保存结果
        if out_type == 'db':
            # 保存到数据库
            out_array = np.column_stack((data[NAME['学生编号']].values, add_list, len(add_list) * [set_month]))
            mk_dataframe_and_save_to_db(data=out_array, contain=OUT_PUT_ADD_LIST_CONTAIN,)
        elif out_type == 'csv':
            # 保存到文件
            out_array = np.column_stack((data[NAME['学生编号']].values, add_list, len(add_list) * [set_month]))
            make_dataframe_to_csv(filename=OUT_PUT_ADD_LIST_FILE_NAME + '_' + set_month + '.csv',
                                  data=out_array,
                                  contain=OUT_PUT_ADD_LIST_CONTAIN, info='积极度模型中间表')
        # 保存结果到文件中
        out_array = np.column_stack((data[NAME['学生编号']].values, activity, len(activity) * [set_month]))
        make_dataframe_to_csv(filename=OUT_PUT_FILE_NAME,
                              data=out_array,
                              contain=OUT_PUT_FILE_CONTAIN, info='积极度模型输出表')
        return out_array

    # 此函数可计算积极度
    def calc_activity(self, data, last_activity, get_add_list=False):
        """积极度计算函数
            参数：
            ----------
            data: array
                学生信息，n行target_num+1列的二维数组，n为学生数，target_num为指标数
            last_activity: array
                上个月的积极度，长度为n的数组，n为学生数
            get_add_list: bool
                是否返回中间表，若为True则返回中间表

            返回值：
            ----------
            activity : array shape=[n]
                积极度，长度为n的数组，n为学生数
            add_list : array
                中间表，n行target_num列的二维数组，n为学生数，target_num为中间表包含的项目数
                若get_add_list为True则返回此项，包含各指标得分，月活跃度，积极度算出值，积极度减分值，积极度输出值
        """

        # 检查输入是否正确
        data = check_array(data, feature_num=self.TARGET_NUM+1)
        last_activity = check_array(last_activity, ensure_2d=False)
        check_matching(data, last_activity)

        # 构造dataframe
        school_name = data[:, 0]
        data = data[:, 1:].astype(np.float64)
        data = pd.DataFrame(data, columns=self.TARGET_NAME)
        data[NAME['高校名称']] = school_name
        data[NAME['上月积极度值']] = last_activity

        # 获取普通计算方式和特殊计算方式的索引
        common_index = data[-data[NAME['高校名称']].isin(SPECIAL_SCHOOL_LIST)].index
        special_index = data[data[NAME['高校名称']].isin(SPECIAL_SCHOOL_LIST)].index

        # 计算普通指标的得分和月活跃度
        common_target_score = self.__target_score(data.loc[common_index][self.TARGET_NAME].values,
                                           self.TARGET_MIN_VAL,
                                           self.TARGET_MAX_VAL) * self.TARGET_WEIGHT
        data.at[common_index, NAME['月活跃度值']] = np.sum(common_target_score, axis=1) / self.MAX_MONTH_ACTIVITY
        # 计算特殊指标的得分和月活跃度
        special_target_score = self.__target_score(data.loc[special_index][self.SPECIAL_TARGET_NAME].values,
                                           self.SPECIAL_TARGET_MIN_VAL,
                                           self.SPECIAL_TARGET_MAX_VAL) * self.SPECIAL_TARGET_WEIGHT
        data.at[special_index, NAME['月活跃度值']] = np.sum(special_target_score, axis=1) / self.SPECIAL_MAX_MONTH_ACTIVITY
        # 拼接普通指标得分和特殊指标得分
        target_score = np.zeros((len(data), self.TARGET_NUM))
        for i in range(len(common_index)):
            target_score[common_index[i]] = common_target_score[i]
        for i in range(len(special_index)):
            target_score[special_index[i]] = special_target_score[i]
        del common_target_score, special_target_score

        # 计算当月能获取的最大积极度值
        data[NAME['积极度最大加分值']] = self.__kernal_func(data[NAME['上月积极度值']].values)

        # 根据月活跃度,上月积极度，积极度最大加分值计算积极度
        data[NAME['积极度分值']] = self.__activity_score(data[NAME['月活跃度值']].values, data[NAME['上月积极度值']].values, data[NAME['积极度最大加分值']])

        # 根据惩罚项进行扣分
        punish_list = PUNISH_RULE(data)
        # 积极度降档
        for punish_item in punish_list:
            if punish_item['PUNISH_ACTIVITY'] != 0:
                data.at[punish_item['PUNISH_INDEX'], NAME['积极度分值']] = punish_item['PUNISH_ACTIVITY']
        activity = np.array(data[NAME['积极度分值']].values)
        # 根据权重扣分
        for punish_item in punish_list:
            data.at[punish_item['PUNISH_INDEX'], NAME['积极度分值']] = self.__punish_score(data.loc[punish_item['PUNISH_INDEX']][NAME['积极度分值']].values,
                                                                                           data.loc[punish_item['PUNISH_INDEX']][NAME['积极度最大加分值']].values,
                                                                                           punish_item['PUNISH_WEIGHT'],
                                                                                           data.loc[punish_item['PUNISH_INDEX']][NAME['月活跃度值']].values)

        # 处理返回结果
        if get_add_list:
            # 中间表，包含各指标得分，月活跃度，积极度最大加分值, 积极度算出值，积极度减分值，积极度输出值
            add_list = np.column_stack((np.round(target_score, 2), np.round(data[NAME['月活跃度值']].values, 2),
                                        data[NAME['积极度最大加分值']].values, activity,
                                        activity - data[NAME['积极度分值']].values, data[NAME['积极度分值']].values))
            activity = data[NAME['积极度分值']].values
            return activity, add_list
        activity = data[NAME['积极度分值']].values
        return activity

    # 指标得分计算函数
    def __target_score(self, value, bottom, top):
        value = np.where(value < top, value, top)
        target_score = (1 - ((value - bottom) / (top - bottom) - 1) ** 2) ** 0.5
        return target_score

    # 积极度得分计算函数
    def __activity_score(self, lam, value, alpha):
        result = lam * alpha + value
        result = np.where(result < MAX_SCORE, result, MAX_SCORE)
        result = np.around(result)
        return result

    # 积极度扣分计算函数
    def __punish_score(self, value, alpha, weight, lam):
        result = value - weight * alpha * (1 - lam)
        result = np.where(result > MIN_SCORE, result, MIN_SCORE)
        result = np.around(result)
        return result

    # 此函数可计算当月能获取的最大积极度值
    def __kernal_func(self, value):
        result = 0.5*(MAX_SCORE - value) - 25
        result = np.where(result < 200, result, 200)
        result = np.where(result > 1, result, 1)
        return result
