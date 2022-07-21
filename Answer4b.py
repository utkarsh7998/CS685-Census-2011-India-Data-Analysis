#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[10]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings("ignore")


# # Reading Total Population for each state/UT

# In[11]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame(columns=['State_code','State_name','Population'])


# In[ ]:


# Reading c-17 data
for i in range(1,36,1):
    if(i<10):
        path = './c-17/DDW-C17-0'+str(i)+'00.XLSX'
    if(i>9):
        path = './c-17/DDW-C17-'+str(i)+'00.XLSX'
    df = pd.read_excel(path, engine='openpyxl')
    df = df[1:]
    df.columns = df.iloc[0]
    df = df[1:]
    df.columns = ['State_code','State_name','Total speakers of languages','Name','Population','Males','Females','Number of speakers speaking subsidiary languages (1st language)','1 st subsidiary languages','Persons','Males','Females','Number of speakers speaking subsidiary languages (2nd language)','2nd subsidiary languages','Persons','Males','Females']
    df = df[3:]
    df = df[['State_code','State_name','Population']]
    df.reset_index(drop=True,inplace=True)
    df.fillna(0,inplace=True)
    d = {}
    d['State_code'] = df.loc[0,'State_code']
    d['State_name'] = df.loc[0,'State_name']
    d['Population'] = df['Population'].sum()
    final = final.append(d, ignore_index = True)
# final


# # Reading Language Data for each state/UT

# In[ ]:


# Reading Data for second and third language from c-18
df = pd.read_excel('DDW-C18-0000.xlsx',engine='openpyxl')
df = df[1:]
df.columns = df.iloc[0]
df = df[1:]
df.columns = ['State_code','District_code','State_name','Rural/Urban','Age-group','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[3:]
df = df[df['State_name']!='INDIA']
df = df[(df['Rural/Urban']=='Total')&(df['Age-group']=='Total')]
df = df.drop(['District_code','Rural/Urban','Age-group'],axis='columns')
df.reset_index(drop=True,inplace=True)
df


# # Concatenating population and language dataframes

# In[ ]:


# Concatenating c-17 and c-18 data
final2 = pd.concat([final, df],axis=1)

# Dropping duplicate columns formed after concatenation
final2 = final2.loc[:,~final2.columns.duplicated()]
final2


# # Finding number of people speaking  
# ## (i) exactly 1 language
# ## (ii) exactly 2 language
# ## (iii) 3 or more language

# In[ ]:


# Making answer dataframe
ans = final2.copy()
ans['Exactly 1 lang'] = ((ans['Population'] - ans['Number speaking second language']))
ans['Exactly 2 lang'] = ((ans['Number speaking second language'] - ans['Number speaking third language']))
ans['3 or more lang'] = (ans['Number speaking third language'])
ans = ans[['State_code','State_name','Exactly 1 lang','Exactly 2 lang','3 or more lang']]
ans
                                                                                        


# In[ ]:


# 2-to-1 ratio
ans_2_to_1 = ans.copy()
ans_2_to_1['Ratio_2_to_1'] = (ans_2_to_1['Exactly 2 lang']/ans_2_to_1['Exactly 1 lang']).astype('float')
ans_2_to_1 = ans_2_to_1[['State_code','State_name','Ratio_2_to_1']]
t = ans_2_to_1.nlargest(3, 'Ratio_2_to_1').reset_index(drop=True)
t = t.append(ans_2_to_1.nsmallest(3, 'Ratio_2_to_1').reset_index(drop=True),ignore_index = True)
t = t.drop('State_name',axis=1)
t


# # Writing output to csv

# In[ ]:


t.to_csv('./2-to-1-ratio.csv', index=False)


# In[ ]:


print("Execution completed")


# In[ ]:




