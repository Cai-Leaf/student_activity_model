"""
积极度模型配置文件
"""

# 定义最高分
MAX_SCORE = 899

# 定义最低分
MIN_SCORE = 350

# 定义初始分
DEFAULT_SCORE = 450

# 定义名称
NAME = {
    '学生编号': 'STUDENTCODE',
    '高校名称': 'UNIVERSITYNAME',
    '月份': 'MONTH',
    '登录次数': 'LOG_NUM',
    '登陆时长': 'LOG_DURATION',
    '登陆天数': 'LOG_DAY',
    '课件点击次数': 'CLICK_COURSE',
    '课程问答发回帖数量': 'T_F',
    '微学吧栏目点击次数': 'C_PV',
    '有效作业数': 'HOMEWORK_NUM',
    '已完成作业数': 'FIN_HOMEWORE_NUM',
    '作业完成度': 'COMPLETION_WORK',
    '积极度分值': 'ACTIVITY',
    '登录次数分数': 'LOG_NUM_SCORE',
    '登陆时长分数': 'LOG_DURATION_SCORE',
    '登陆天数分数': 'LOG_DAY_SCORE',
    '课件点击次数分数': 'CLICK_COURSE_SCORE',
    '课程问答发回帖数量分数': 'T_F_SCORE',
    '微学吧栏目点击次数分数': 'C_PV_SCORE',
    '作业完成度分数': 'COMPLETION_WORK_SCORE',
    '月活跃度值': 'MONTH_ACTIVITY',
    '积极度算出值': 'CALC_ACTIVITY',
    '积极度减分值': 'CUT_ACTIVITY',
    '上月积极度值': 'LAST_ACTIVITY',
    '积极度最大加分值': 'ALPHA'
}

# 定义普通指标的权重及范围
TARGET_WEIGHT_RANGE = [
    # 登录次数
    {
        'NAME': NAME['登录次数'],
        'WEIGHT': 100,
        'MAX_VAL': 10,
        'MIN_VAL': 0,
    },

    # 登录时长
    {
        'NAME': NAME['登陆时长'],
        'WEIGHT': 150,
        'MAX_VAL': 3600,
        'MIN_VAL': 0,
    },

    # 登录天数
    {
        'NAME': NAME['登陆天数'],
        'WEIGHT': 100,
        'MAX_VAL': 8,
        'MIN_VAL': 0,
    },

    # 点击次数_课件
    {
        'NAME': NAME['课件点击次数'],
        'WEIGHT': 150,
        'MAX_VAL': 10,
        'MIN_VAL': 0,
    },

    # 发回帖数量_课程问答
    {
        'NAME': NAME['课程问答发回帖数量'],
        'WEIGHT': 100,
        'MAX_VAL': 8,
        'MIN_VAL': 0,
    },

    # 栏目点击次数_微学吧
    {
        'NAME': NAME['微学吧栏目点击次数'],
        'WEIGHT': 100,
        'MAX_VAL': 15,
        'MIN_VAL': 0,
    },

    # 作业完成度
    {
        'NAME': NAME['作业完成度'],
        'WEIGHT': 100,
        'MAX_VAL': 1,
        'MIN_VAL': 0,
    }
]

# 定义特殊指标的权重及范围
SPECIAL_TARGET_WEIGHT_RANGE = [
    # 登录次数
    {
        'NAME': NAME['登录次数'],
        'WEIGHT': 100,
        'MAX_VAL': 10,
        'MIN_VAL': 0,
    },

    # 登录时长
    {
        'NAME': NAME['登陆时长'],
        'WEIGHT': 150,
        'MAX_VAL': 3600,
        'MIN_VAL': 0,
    },

    # 登录天数
    {
        'NAME': NAME['登陆天数'],
        'WEIGHT': 100,
        'MAX_VAL': 8,
        'MIN_VAL': 0,
    },

    # 点击次数_课件
    {
        'NAME': NAME['课件点击次数'],
        'WEIGHT': 0,
        'MAX_VAL': 10,
        'MIN_VAL': 0,
    },

    # 发回帖数量_课程问答
    {
        'NAME': NAME['课程问答发回帖数量'],
        'WEIGHT': 0,
        'MAX_VAL': 8,
        'MIN_VAL': 0,
    },

    # 栏目点击次数_微学吧
    {
        'NAME': NAME['微学吧栏目点击次数'],
        'WEIGHT': 0,
        'MAX_VAL': 15,
        'MIN_VAL': 0,
    },

    # 作业完成度
    {
        'NAME': NAME['作业完成度'],
        'WEIGHT': 0,
        'MAX_VAL': 1,
        'MIN_VAL': 0,
    }
]


# 定义减分规则
def PUNISH_RULE(data):
    punish_list = [
        # 积极度得分在350到450之间，登录次数小于1，扣除相应月活跃度，PUNISH_ACTIVITY=0 表示从原值开始扣分
        {
            'PUNISH_INDEX': data[(data[NAME['登录次数']] < 1) &
                                 ((data[NAME['积极度分值']] > 350) & (data[NAME['积极度分值']] < 450))].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 0
        },

        # 积极度得分在450到500之间，登录次数小于1，扣除相应月活跃度，PUNISH_ACTIVITY=450 表示从450开始扣分
        {
            'PUNISH_INDEX': data[(data[NAME['登录次数']] < 1) &
                                 ((data[NAME['积极度分值']] >= 450) & (data[NAME['积极度分值']] < 500))].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 450
        },

        # 积极度得分在450到500之间，登录时长小于5分钟（300秒），扣除相应月活跃度
        {
            'PUNISH_INDEX': data[(data[NAME['登陆时长']] < 300) &
                                 ((data[NAME['积极度分值']] >= 450) & (data[NAME['积极度分值']] < 500))].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 450
        },

        # 积极度得分在500到600之间，登录次数小于3，扣除相应月活跃度
        {
            'PUNISH_INDEX': data[(data[NAME['登录次数']] < 3) &
                                 ((data[NAME['积极度分值']] >= 500) & (data[NAME['积极度分值']] < 600))].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 500
        },

        # 积极度得分在500到600之间，登录时长小于30分钟（1800秒），扣除相应月活跃度
        {
            'PUNISH_INDEX': data[(data[NAME['登陆时长']] < 1800) &
                                 ((data[NAME['积极度分值']] >= 500) & (data[NAME['积极度分值']] < 600))].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 500
        },

        # 积极度得分在600以上，登录次数小于6，扣除相应月活跃度
        {
            'PUNISH_INDEX': data[(data[NAME['登录次数']] < 6) &
                                 (data[NAME['积极度分值']] >= 600)].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 600
        },

        # 积极度得分在600以上，登录时长小于60分钟（3600秒），扣除相应月活跃度
        {
            'PUNISH_INDEX': data[(data[NAME['登陆时长']] < 3600) &
                                 (data[NAME['积极度分值']] >= 600)].index,
            'PUNISH_WEIGHT': 0.1,
            'PUNISH_ACTIVITY': 600
        }
    ]
    return punish_list

# 定义输入的用户信息所包含的内容
INPUT_DATA_CONTAIN = [
    NAME['学生编号'],
    NAME['高校名称'],
    NAME['登录次数'],
    NAME['登陆时长'],
    NAME['登陆天数'],
    NAME['课件点击次数'],
    NAME['课程问答发回帖数量'],
    NAME['微学吧栏目点击次数'],
    NAME['有效作业数'],
    NAME['已完成作业数'],
]

# 定义输入的中间表文件所包含的内容
INPUT_ADD_LIST_FILE_CONTAIN = [
    NAME['学生编号'],
    NAME['积极度分值']
]

# 定义输出文件所包含的内容
OUT_PUT_FILE_CONTAIN = [
    NAME['学生编号'],
    NAME['积极度分值'],
    NAME['月份']
]

# 定义输出的中间表所包含的内容
OUT_PUT_ADD_LIST_CONTAIN = [
    NAME['学生编号'],
    NAME['登录次数分数'],
    NAME['登陆时长分数'],
    NAME['登陆天数分数'],
    NAME['课件点击次数分数'],
    NAME['课程问答发回帖数量分数'],
    NAME['微学吧栏目点击次数分数'],
    NAME['作业完成度分数'],
    NAME['月活跃度值'],
    NAME['积极度最大加分值'],
    NAME['积极度算出值'],
    NAME['积极度减分值'],
    NAME['积极度分值'],
    NAME['月份']
]

# 定义需要用特殊指标来建模的学校
SPECIAL_SCHOOL_LIST = [
    '北京大学',
    '对外经济贸易大学',
    '西南大学',
    '中国人民大学',
    '中国石油大学（北京）',
    '中南大学',
    '北京外国语大学',
    '北京邮电大学',
    '江南大学',
    '西南交通大学',
    '中国传媒大学',
]

# 定义输入文件名
INPUT_FILE_NAME = 'activity_out_before.csv'

# 定义积极度输出文件名
OUT_PUT_FILE_NAME = 'activity_out_before.csv'

# 定义中间表输出文件名
OUT_PUT_ADD_LIST_FILE_NAME = 'add_list_out'

