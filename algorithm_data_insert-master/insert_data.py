import pymysql
db = pymysql.connect(host="XXXX", user="XX", passwd="XXX", db="XX",
                     port=XXX, charset='utf8')
cursor = db.cursor()
def insert_info(pro_wer,pro_cer,pro_version,engineering_wer,engineering_cer,engineering_vesion,modle_name,modle_wer,modle_cer,modle_version,update_time,data_set,capacity_wav,capacity_mp4,delay_time,online_time,valid):
    """
    向数据库中插入数据的函数
    :param pro_wer:
    :param pro_cer:
    :param pro_version:
    :param engineering_wer:
    :param engineering_cer:
    :param engineering_vesion:
    :param modle_name:
    :param modle_wer:
    :param modle_cer:
    :param modle_version:
    :param update_time:
    :param data_set:
    :param capacity_wav:
    :param capacity_mp4:
    :param delay_time:
    :param online_time:
    :param valid:
    :return:
    """
    sql = "insert into TestResult(pro_wer,pro_cer,pro_version,engineering_wer,engineering_cer,engineering_vesion,modle_name,modle_wer,modle_cer,modle_version,update_time,data_set,capacity_wav,capacity_mp4,delay_time,online_time,valid) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (pro_wer,pro_cer,pro_version,engineering_wer,engineering_cer,engineering_vesion,modle_name,modle_wer,modle_cer,modle_version,update_time,data_set,capacity_wav,capacity_mp4,delay_time,online_time,valid))  # 列表格式数据
        # cursor.execute(sql)
        db.commit()
        # result = cursor.fetchall()
        # for i in result:
        #     print(i)
        # print(result)
        # print(db.commit())
        return ('insert success')
    except Exception as e:
        print(e)
        db.rollback()
        return e
    db.close()

if __name__ == "__main__":
    insert_info(00,00,'xxx',00,00,'xxx','',xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx,xxx)