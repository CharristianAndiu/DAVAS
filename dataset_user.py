import pymysql
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user="root",
                       passwd="123456",
                        db="user_data",
                       charset="utf8mb4"
                       )
# 获取游标
cursor = conn.cursor()
#创建表格
sql = "CREATE TABLE users(username TEXT,email TEXT,full_name TEXT,disabled BOOL,password TEXT)"
try:
    cursor.execute(sql)
    conn.commit()
except:
    print("表已存在")
print('成功创建表格')

# 插入数据
sql = "INSERT INTO users VALUES('%s','%s','%s',%d,'%s')"
data = ("zhangsan","zhangsan@gmail","zhangsan",0,"123456")
find_sql = "SELECT * FROM users WHERE email = '%s'"
find_data = (data[1])
cursor.execute(find_sql % find_data)
for row in cursor.fetchall():
    continue
if cursor.rowcount == 0 :
    cursor.execute(sql % data)
    conn.commit()
    print('成功插入', cursor.rowcount, '条数据')
else:
    print('the user has exist')

# 修改数据
sql = "UPDATE users SET password = '%s' WHERE email = '%s' "
data = ('12345678', 'zhangsan@gmail')
cursor.execute(sql % data)
conn.commit()
print('成功修改', cursor.rowcount, '条数据')

# 查询数据
sql = "SELECT * FROM users WHERE email = '%s'"
data = ('zhangsan@gmail')
cursor.execute(sql % data)
for row in cursor.fetchall():
    print("%s" % str(row))
print('共查找出', cursor.rowcount, '条数据')

# # 删除数据
# sql = "DELETE FROM student WHERE id = %d LIMIT %d"
# data = (1, 1)
# cursor.execute(sql % data)
# connect.commit()
# print('成功删除', cursor.rowcount, '条数据')

# # 事务处理
# sql_1 = "UPDATE student SET name = name + '1' WHERE id = 1 "
#
# try:
#     cursor.execute(sql_1)
# except Exception as e:
#     connect.rollback()  # 事务回滚
#     print('事务处理失败', e)
# else:
#     connect.commit()  # 事务提交
#     print('事务处理成功', cursor.rowcount)

# 关闭连接
cursor.close()
conn.close()
