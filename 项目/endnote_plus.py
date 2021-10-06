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
# tree=[]
# for i in range(0,26):
#     alphabet=chr(ord('a')+i)
#     tree.append(pickle.load(open('terms/tree.'+alphabet,'rb')))
# tree.append(pickle.load(open('terms/tree._','rb')))
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
    i=ord(term[0].lower())-ord('a')
#     if i in range(0,26):
#         t=sorted(tree[i].find(Item(term, term), 100))
#     else:
#         t=sorted(tree[26].find(Item(term, term), 100))
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
#       title=normalize(str(title[0]))
#         print(chardet.detect(str.encode(command)))
            c.execute(command)


# In[48]:


# Create table c.execute('''CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost. conn.close()


# In[49]:


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
    journals_handle(c)#title_handle(c)
    
    conn.commit()
    


# In[25]:


c.execute('PRAGMA table_info(refs)')
print(c.fetchall())


# In[52]:


print(sorted(tree.find(Item("International Conference on Mathematical Modeling in Physical Science"," term"), 50))[0])


# In[ ]:


conn.close()

