"""
用于数据库的存取
"""
import pandas as pd
import cx_Oracle


def mk_dataframe_and_save_to_db(data, contain):
    try:
        data = pd.DataFrame(data, columns=contain)
    except ValueError:
        raise ValueError('创建DataFrame失败，参数错误')
    # 插入数据库
    db = cx_Oracle.connect('用户名', '密码', 'ip:1521/oracle的serve_name')
    cursor = db.cursor()
    try:
        # 创建column_name 形式如"STUDENTCODE, LOG_NUM_SCORE, LOG_DURATION_SCORE, LOG_DAY_SCORE..."
        # 创建value_name 形式如":1, :2, :3, :4..."
        column_name = ''
        value_name = ''
        for i in range(len(contain)):
            if i != len(contain)-1:
                column_name += contain[i] + ', '
                value_name += ':' + str(i+1) + ', '
            else:
                column_name += contain[i]
                value_name += ':' + str(i+1)
        param = []
        for indexs in data.index:
            param.append(tuple(data.loc[indexs].values))
        # 类似于 insert into table_name(STUDENTCODE, LOG_NUM_SCORE, LOG_DURATION_SCORE, 'LOG_DAY_SCORE...) values(:1, :2, :3, :4, ...)
        cursor.prepare('insert into table_name(' + column_name + ') values(' + value_name + ')')
        cursor.executemany(None, param)
        db.commit()
    except Exception as e:
        raise ValueError('数据库插入失败', e)
    finally:
        cursor.close()
        db.close()
    print('模型结果已存入数据库')
    return
