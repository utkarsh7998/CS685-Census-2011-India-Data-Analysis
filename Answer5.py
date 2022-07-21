#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[1]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings("ignore")


# # Reading Population for each age group for each state/UT

# In[2]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame(columns=[ 'State_code', 'Age 5-9','Age 10-14', 'Age 15-19', 'Age 20-24', 'Age 25-29', 'Age 30-49',
        'Age 50-69', 'Age 70+', 'Age not stated'])


# In[3]:


# Reading c-14 data
for i in range(0,36,1):
    if(i<10):
        path = './c-14/DDW-0'+str(i)+'00C-14.xls'
    if(i>9):
        path = './c-14/DDW-'+str(i)+'00C-14.xls'
    df = pd.read_excel(path, sheet_name='Sheet1')
    df.columns = ['Table_name','State_code','Dist_code','State_name','Age-group','Total_Persons','Total_Males','Total_Females','Rural_Persons','Rural_Males','Rural_Females','Urban_Persons','Urban_Males','Urban_Females']
    df = df[7:]
    df = df[df['Dist_code']=='000']
    df.reset_index(drop=True,inplace=True)
    df.fillna(0,inplace=True)    
    d = {}
    d['State_code'] = df.loc[0,'State_code']
    d['State_name'] = df.loc[0,'State_name']
    d['Age 5-9'] = df.loc[1,'Total_Persons']
    d['Age 10-14'] = df.loc[2,'Total_Persons']
    d['Age 15-19'] = df.loc[3,'Total_Persons']
    d['Age 20-24'] = df.loc[4,'Total_Persons']
    d['Age 25-29'] = df.loc[5,'Total_Persons']
    d['Age 30-49'] = df.loc[6,'Total_Persons'] + df.loc[7,'Total_Persons'] + df.loc[8,'Total_Persons'] + df.loc[9,'Total_Persons'] 
    d['Age 50-69'] = df.loc[10,'Total_Persons'] + df.loc[11,'Total_Persons'] + df.loc[12,'Total_Persons'] + df.loc[13,'Total_Persons']  
    d['Age 70+']   = df.loc[14,'Total_Persons'] + df.loc[15,'Total_Persons'] + df.loc[16,'Total_Persons']
    d['Age not stated'] = df.loc[17, 'Total_Persons']
    final = final.append(d, ignore_index=True)
final


# # Reading language data

# In[4]:


# Reading Data for  third language from c-18
df = pd.read_excel('DDW-C18-0000.xlsx',engine='openpyxl')
df = df[1:]
df.columns = df.iloc[0]
df = df[1:]
df.columns = ['State_code','District_code','State_name','Rural/Urban','Age-group','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[3:]
df = df[(df['Age-group']!='Total')]
df = df[df['Rural/Urban']=='Total']
df = df.iloc[:,[0,2,4,8]]
df.reset_index(drop=True,inplace=True)
df.head(10)


# # Merging Language and Population data for each age group for each state/UT

# In[5]:


vals = set(df['Age-group'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Age-group']==i]
    t = t[['State_name','Number speaking third language']]
    t.columns = ['State_name','3+ lang in '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
final


# In[6]:


final.columns


# # Finding percenatage of 3+ language speaking people in each age group for each state/UT

# In[7]:


final2 = final.copy()
final2['age 5-9'] = (final2['3+ lang in 5-9']*100)/final2['Age 5-9']
final2['age 10-14'] = (final2['3+ lang in 10-14']*100)/final2['Age 10-14']
final2['age 15-19'] = (final2['3+ lang in 15-19']*100)/final2['Age 15-19']
final2['age 20-24'] = (final2['3+ lang in 20-24']*100)/final2['Age 20-24']
final2['age 25-29'] = (final2['3+ lang in 25-29']*100)/final2['Age 25-29']
final2['age 30-49'] = (final2['3+ lang in 30-49']*100)/final2['Age 30-49']
final2['age 50-69'] = (final2['3+ lang in 50-69']*100)/final2['Age 50-69']
final2['age 70+'] = (final2['3+ lang in 70+']*100)/final2['Age 70+']
final2['age Age not stated'] = (final2['3+ lang in Age not stated']*100)/final2['Age not stated']
final2 = final2[['State_code','State_name','age 5-9','age 10-14','age 15-19','age 20-24','age 25-29','age 30-49','age 50-69','age 70+','age Age not stated']]
final2


# # Finding maximum for each row and their column names

# In[8]:


temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['max value'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['max age group'] = temp2.idxmax(axis=1, skipna=True)
final2


# # Final Output dataframe

# In[9]:


ans = final2.copy()
ans = ans[['State_code','max age group','max value']]
ans['max age group'] = ans['max age group'].apply(lambda x: x.split(' ')[1])
ans.columns = ['state/ut','age-group','percentage']
ans


# # Writing output to csv file

# In[10]:


ans.to_csv('./age-india.csv', index=False)


# In[11]:


print("Execution completed")


# In[ ]:




