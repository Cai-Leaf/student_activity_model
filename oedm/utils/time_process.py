"""
用于处理时间
"""

import datetime


def get_last_month_date():
    """
        获取上个月的年月值
    """
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    res = datetime.datetime(year, month, 1).strftime('%Y-%m')
    return res
