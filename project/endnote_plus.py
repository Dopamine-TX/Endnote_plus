#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sqlite3
from collections import namedtuple
import collections
import string
#import chardet
import os
import re
import pickle


# In[3]:


Item = collections.namedtuple('Item', 'abb all_w')
tree=pickle.load(open('terms/terms.tree','rb'))


# In[4]:


'''读文件'''
def read_file(filepath):
    with open(filepath) as fp:
        content=fp.read();
    return content


# In[5]:


'''首字母大写其余小写,去除末尾非字母符号'''
def normalize(s):
    punctuation = ".,!;:'\"/<>，；：！‘’"
    s=s[0].upper() + s[1:].lower()
    if s[-1] in punctuation:
        print("有非法标点")
        return s[:-1]
    return s


# In[50]:


'''获取期刊全名'''
def get_journal(term):
    t=sorted(tree.find(Item(term, term), 0))#！！！这里调节。！！！
    try:#不一定有解
        print(t[0])
        return t[0][1].all_w
    except:
        print("error")
        return "error"


# In[46]:


'''处理标题的功能函数-1'''
def title_handle(c):
    c.execute('SELECT title FROM refs')
    titles=c.fetchall()
    i=1
    for title in titles:
        title=normalize(str(title[0]))
        command='UPDATE refs SET title = "'+title+ '" where ID='+str(i)
        try:
            c.execute(command)
            print(command)
        except:
            print('错误！')
        i+=1    


# In[47]:


def journals_handle(c):
    c.execute('SELECT secondary_title FROM refs')
    journals=c.fetchall()
    i=1
    for journal in journals:
        if journal[0]:
            print(journal[0])
            journal_=get_journal(journal[0])
            command='UPDATE refs SET secondary_title = "'+journal_+ '" where ID='+str(i)
            c.execute(command)




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
    journals_handle(c)

    conn.commit()
    conn.close()

