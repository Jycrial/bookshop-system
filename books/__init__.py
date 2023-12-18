from flask import Flask
import pymysql

"""
数据库
"""

# 连接mysql并选择book数据库
def get_db_conn():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        # 请输入你的本地mysql密码
        password='******',
        charset='utf8mb4',
        database='books'
    )
    return conn

# 查询所有数据返回字典列表
def select_all_as_dict(sql: str):
    with get_db_conn() as conn:
        with conn.cursor() as cs:
            cs.execute(sql)
            result = cs.fetchall()

            # 获取列名
            columns = [desc[0] for desc in cs.description]
            # 转化成字典列表
            data_as_dict = [dict(zip(columns, data)) for data in result]
    return data_as_dict

"""
应用
"""

# 创建应用
app = Flask(__name__)
# 加密
app.config['SECRET_KEY'] = "WangCong's work"

from books import urls