import re
import pymysql
from datetime import datetime, timedelta, date
#将爬取的内容插入sql
now = datetime.now()
oneday = timedelta(days=1)
nday = timedelta(days=0)
today = datetime(now.year, now.month, now.day) - nday
yesterday = today - oneday - nday
count = 493
db = pymysql.connect(host="xxx.xxx.xxx.xx", user="user_name", passwd="password", db="database_name",
                     port=xxx, charset='utf8')
cursor = db.cursor()
sql = "INSERT INTO  new_table(day ,count )\
        VALUES ('%s', %s)" % \
      (yesterday, count)
try:
    cursor.execute(sql)
    db.commit()
    print("done")
except:
    db.rollback()
db.close()
