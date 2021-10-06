#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import os
from collections import namedtuple
import collections
import pybktree
import editdistance


# In[2]:


a='911a'
if ord(a[0]) in range(ord('0'),ord('9')+1):
    print("!!")


# In[3]:


import cloudpickle
def item_distance(x, y):
    #return pybktree.hamming_distance(x.bits, y.bits)
    return editdistance.eval(x.abb.lower(), y.abb.lower())#统一用小写来比较


# In[8]:


files= os.listdir('Terms List')
Item = collections.namedtuple('Item', 'abb all_w')
files.remove('.ipynb_checkpoints')
# for i in range(24,26):
#     alphabet=chr(ord('a')+i)
#     print(alphabet)
tree = pybktree.BKTree(item_distance, [Item("0", '3e Millenaire')])
for file in files: #遍历文件夹
    path="Terms List/"+file
    print(file)
    with open(file=path, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            terms=line.rstrip().split('	')
            journal=terms[0]#保存全写
            for term in terms:#有莫名其妙的换行符，所以要rstrip()
                if ord(term[0].lower()) not in range(ord('a'),ord('z')+1):#if term[0].lower()==alphabet:#if ord(term[0]) in range(ord('0'),ord('9')+1):#
                    print(term)
                    tree.add(Item(term,journal))
    f.close()
#         with open('terms/tree.'+alphabet,"wb") as file:
#             pickled_lambda = cloudpickle.dump(tree,file)
        


# In[5]:


print(files)


# In[6]:


files.remove('.ipynb_checkpoints')


# In[ ]:


print(sorted(tree))


# In[ ]:


pickle.dump(tree,'Terms List/tree.a')


# In[11]:



with open('terms/tree._',"wb") as file:
    pickled_lambda = cloudpickle.dump(tree,file)#pickle.dump(pickled_lambda, file, True)


# In[ ]:


pickled_lambda = cloudpickle.dump(tree,file)


# In[ ]:


pickled_lambda=pickle.load(open('Terms List/tree.a','rb'))


# In[ ]:


tree = pybktree.BKTree(pybktree.hamming_distance, ['banana', 'bahana','fsfg','fgdh'])
tree.add("131")              # add element 15
sorted(tree)              # BKTree instances are iterable
sorted(tree.find('Debreceni. Déri. Móz. êvk.',110))


# In[ ]:


Item = collections.namedtuple('Item', 'bits id')
def item_distance(x, y):
    #return pybktree.hamming_distance(x.bits, y.bits)
    return editdistance.eval(x.bits, y.bits)
tree = pybktree.BKTree(item_distance, [Item('A Debreceni Déri Mózeum évkînyve', 'a'), Item('bahana', 'b'),
                                           Item('fsfg', 'c'), Item('fgdh', 'd')])
tree.add(Item("131", 'e'))
sorted(tree.find(Item('Debreceni. Déri. Móz. êvk.', 'x'), 100))
# [(1, Item(bits=5, id='c')), (1, Item(bits=15, id='e'))]


# In[ ]:


tree=pickle.load(open('Terms List/a.tree','rb'))
sorted(tree.find(Item('Debreceni. Déri. Móz. êvk.', 'x'), 100))


# In[ ]:




