#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import os
from collections import namedtuple
import collections
import pybktree
import editdistance



import cloudpickle
def item_distance(x, y):
    return editdistance.eval(x.abb.lower(), y.abb.lower())#统一用小写来比较

terms_files= os.listdir('Terms List')
Item = collections.namedtuple('Item', 'abb all_w')

terms_files('.ipynb_checkpoints')
#不在juypter notebook的环境运行可能要删掉这一句

tree = pybktree.BKTree(item_distance, [Item("a", '3e Millenaire')])
for term_file in term_files: #遍历文件夹
    path="Terms List/"+term_file
    print(term_file)
    with open(file=path, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            terms=line.rstrip().split('\t')#有莫名其妙的换行符，所以要rstrip()
            journal=terms[0]#保存全写
            for term in terms:
                print(term)
                tree.add(Item(term,journal))
    f.close()
with open('terms/terms.tree',"wb") as file:
    pickled_lambda = cloudpickle.dump(tree,file)
        


