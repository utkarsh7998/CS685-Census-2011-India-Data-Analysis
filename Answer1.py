#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings("ignore")


# # Reading Total Population for each state/UT

# In[10]:


# Data Frame containing population for each State/UT
final = pd.DataFrame(columns=['State_code','State_name','Population'])


# In[11]:


# Reading c-17 data
for i in range(0,36,1):
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
final


# # Reading population of 2 lang speaking and 3 language speaking for each state/UT

# In[12]:


# Reading Data for second and third language from c-18
df = pd.read_excel('DDW-C18-0000.xlsx',engine='openpyxl')
df = df[1:]
df.columns = df.iloc[0]
df = df[1:]
df.columns = ['State_code','District_code','State_name','Rural/Urban','Age-group','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[3:]
df = df[(df['Rural/Urban']=='Total')&(df['Age-group']=='Total')]
df = df.drop(['District_code','Rural/Urban','Age-group'],axis='columns')
df.reset_index(drop=True,inplace=True)
df


# # Concatenating Population and Language Dataframe

# In[13]:


# Concatenating c-17 and c-18 data
final2 = pd.concat([final, df],axis=1)

# Dropping duplicate columns formed after concatenation
final2 = final2.loc[:,~final2.columns.duplicated()]
final2


# # Dataframe storing no. of people speaking
# # (i) Exactly 1 language
# # (i) Exactly 2 language
# # (i) 3 or more language for each state/UT

# In[14]:


# Making answer dataframe
ans = final2.copy()
ans['Exactly 1 lang'] = ((ans['Population'] - ans['Number speaking second language'])*100)/(ans['Population'])
ans['Exactly 2 lang'] = ((ans['Number speaking second language'] - ans['Number speaking third language'])*100)/(ans['Population'])
ans['3 or more lang'] = (ans['Number speaking third language']*100)/(ans['Population'])
ans = ans[['State_code','State_name','Exactly 1 lang','Exactly 2 lang','3 or more lang']]
ans
                                                                                        


# # Writing output to csv file

# In[15]:


ans = ans.drop('State_name',axis=1)
ans.columns = ['state-code', 'percent-one' , 'percent-two', 'percent-three']
ans.to_csv('./percent-india.csv',index=False)
ans


# In[16]:


print("Execution completed")


# In[ ]:




