#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import xml.etree.ElementTree as ET
import re
import csv


# In[2]:


xml_list = ['a_lvr_land_a.xml', 'b_lvr_land_a.xml', 'e_lvr_land_a.xml', 'f_lvr_land_a.xml', 'h_lvr_land_a.xml']

for times in range(len(xml_list)):
    tree = ET.parse(xml_list[times])
    root = tree.getroot()
    col_name = []

    for first in root:
        for second in first:
            col_name.append(second.tag)

    col_name = list(sorted(set(col_name), key=col_name.index)) #1. sorted
    df = pd.DataFrame(columns=col_name)
    tmp = 0
    for i in range(len(root)):
        for j in col_name:
            df.loc[i, j] = root[i][tmp].text #2. could not convert string to float
            tmp += 1
            print(df.loc[i, j])
        tmp = 0
        
    if times == 0:
        df_a = df
    elif times == 1:
        df_b = df
    elif times == 2:
        df_e = df
    elif times == 3:
        df_f = df
    else:
        df_h = df


# In[3]:


dataframe_list = [df_a, df_b, df_e, df_f, df_h]
df_all = pd.concat(dataframe_list, ignore_index=True)


# In[4]:


df_filter_a = pd.DataFrame(columns=col_name)
tmp = 0
for i in range(len(df_all)):
    if df_all.loc[i, '主要用途'] == '住家用' and re.search('住宅大樓', df_all.loc[i, '建物型態']) \ 
      and (re.search('...', df_all.loc[i, '總樓層數']) or re.search('....', df_all.loc[i, '總樓層數'])) \
      and not(re.search('^十二', df_all.loc[i, '總樓層數']) or re.search('^十一', df_all.loc[i, '總樓層數'])):
        df_filter_a.loc[tmp] = df_all.loc[i]
        tmp += 1
        
df_filter_a = df_filter_a.reset_index(drop = True)


# In[7]:


df_filter_a.to_csv('filter_a.csv', encoding='utf-8')


# In[17]:


df_filter_b = pd.DataFrame(columns=['總件數', '總車位數', '平均總價元', '平均車位總價元'])

#總件數
total_deal = len(df_all)

#總車位數
car_num = 0
for i in range(len(df_all)):
    tmp = df_all.loc[i, '交易筆棟數'][-1]
    car_num = car_num + int(tmp)
    
#平均總價元
total_cost = 0
for i in range(len(df_all)):
    tmp = df_all.loc[i, '總價元']
    total_cost = total_cost + int(tmp)
    
avg_cost = total_cost/total_deal

#平均車位總價元
car_cost = 0
for i in range(len(df_all)):
    tmp = df_all.loc[i, '車位總價元']
    car_cost = car_cost + int(tmp)
    
avg_car_cost = car_cost/car_num

df_filter_b.loc[0] = [total_deal, car_num, avg_cost, avg_car_cost]


# In[18]:


df_filter_b.to_csv('filter_b.csv', encoding='utf-8')


# In[ ]:




