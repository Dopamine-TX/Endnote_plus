#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
from collections import namedtuple
import string
#import chardet
import os
import subprocess
import re


# In[2]:


# '''自定义排序函数'''
# def my_collate(str1,str2):
#     if st1[1: -1] == st2[1: -1]:
#         return 0
#     elif st1[1: -1] > st2[1: -1]:
#         return 1 
#     else: 
#         return -1

'''读文件'''
def read_file(filepath):
    with open(filepath) as fp:
        content=fp.read();
    return content


# In[3]:


'''首字母大写其余小写,去除末尾非字母符号'''
def normalize(s):
    punctuation = ".,!;:'\"/<>，；：！‘’"
    s=s[0].upper() + s[1:].lower()
    if s[-1] in punctuation:
        print("有非法标点")
        return s[:-1]
    return s


# In[4]:


'''处理标题的功能函数-1'''
def title_handle(c):
    c.execute('SELECT title FROM refs')
    titles=c.fetchall()

    i=1
    for title in titles:
        title=normalize(str(title[0]))
        command='UPDATE refs SET title = "'+title+ '" where ID='+str(i)            
#         print(command)
#         print(chardet.detect(str.encode(command)))
        c.execute(command)
#         try:
#             c.execute(command)
#             print(command)
#         except:
#             print('错误！')
#这里全报错，所以就注释掉了
        i+=1    


# In[5]:


# Create table c.execute('''CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost. conn.close()


# In[6]:


if __name__ == '__main__':
    
    #数据库预处理
    '''基本逻辑把出bug的先删掉，再弄回去'''
    os.system("sqlite3 < out.cmd")
    
    sql=read_file('tmp.sql')    
    f=open('del.sql')
    lines=f.readlines()
    for line in lines:
        sql = sql.replace(line, '')
        
    text_file = open("tmp.sql", 'w')
    text_file.write(sql)
    
    os.system("sqlite3 < in.cmd")
    #反正也不是什么海量数据，应该不用考虑优化吧，暴力yyds！

    #链接数据库与获取游标
    conn = sqlite3.connect('sdb2.db')
    c = conn.cursor()
    
    #sqlite3.dump()没有这样的接口
    #conn.create_collation('ENCIN_zh_CN', my_collate)
    #endnote可能自定义了这个排序规则，所以我补了一下，没想到它还有更多自定义的东西（
    
##获取目标表名
#     c.execute('SELECT name FROM sqlite_master WHERE type="table" order by name')
#     table_names=c.fetchall()
#     print(table_names)
#     for name in table_names:
#         print(name)

# #输出表结构
#     c.execute('PRAGMA table_info(refs)')
#     print(c.fetchall())
    
    #论文名格式处理
    title_handle(c)
    
    conn.commit()
    conn.close()


# In[ ]:





# In[ ]:




