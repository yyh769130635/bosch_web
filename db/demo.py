# encoding: utf-8
'''
@Author:peter young
@file: demo.py
@time: 2020/7/15 21:20
'''

import sqlite3
import os
# print(os.getcwd())
# 上级目录
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 打开数据库连接
conn = sqlite3.connect('test.sqlite3')
print("Opend database successfully")

# ##清除已存在的表 -students
# conn.execute('''DROP TABLE students''');
# conn.commit()

##创建一个表students
conn.execute('''CREATE TABLE students
		(ID INT PRIMARY KEY NOT NULL,
		NAME         TEXT  NOT NULL,
		AGE          INT   NOT NULL);''')
print("Table created successfully");
#
conn.commit()

##插入数据
conn.execute("INSERT INTO sTudents(ID,NAME,AGE)\
		VALUES(1,'Allen',25)");
conn.execute("INSERT INTO sTudents(ID,NAME,AGE)\
		VALUES(2,'Maxsu',20)");
conn.execute("INSERT INTO sTudents(ID,NAME,AGE)\
		VALUES(3,'Teddy',24)");

conn.commit()
print("Records Insert successfully");
print("-------------------");

# ##读取表students
# cursor =conn.execute("SELECT * from students")
# print ("ID NAME AGE")
# for it in cursor:
# 	for i in range(len(it)):
# 		print(it[i])
# 	print ('\n')
# conn.close()