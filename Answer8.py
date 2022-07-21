#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings('ignore')


# # Reading Population for each age group for each state/UT

# In[2]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame()


# In[3]:


# Reading C-14 data
for i in range(0,36,1):
    if(i<10):
        path = './c-14/DDW-0'+str(i)+'00C-14.xls'
    if(i>9):
        path = './c-14/DDW-'+str(i)+'00C-14.xls'
    df = pd.read_excel(path, sheet_name='Sheet1')
#     df = df[1:]
#     df.columns = df.iloc[0]
#     df = df[1:]
    df.columns = ['Table_name','State_code','Dist_code','State_Name','Age-group','Total_Persons','Total_Males','Total_Females','Rural_Persons','Rural_Males','Rural_Females','Urban_Persons','Urban_Males','Urban_Females']
    df = df[7:]
    df = df[df['Dist_code']=='000']
    df.reset_index(drop=True,inplace=True)
    df.fillna(0,inplace=True)    
    d = {}
    d['State_code'] = df.loc[0,'State_code']
#     d['Males in all ages'] = df.loc[0,'Total_Males']
    d['Males in Age 5-9'] = df.loc[1,'Total_Males']
    d['Males in Age 10-14'] = df.loc[2,'Total_Males']
    d['Males in Age 15-19'] = df.loc[3,'Total_Males']
    d['Males in Age 20-24'] = df.loc[4,'Total_Males']
    d['Males in Age 25-29'] = df.loc[5,'Total_Males']
    d['Males in Age 30-49'] = df.loc[6,'Total_Males'] + df.loc[7,'Total_Males'] + df.loc[8,'Total_Males'] + df.loc[9,'Total_Males'] 
    d['Males in Age 50-69'] = df.loc[10,'Total_Males'] + df.loc[11,'Total_Males'] + df.loc[12,'Total_Males'] + df.loc[13,'Total_Males']  
    d['Males in Age 70+']   = df.loc[14,'Total_Males'] + df.loc[15,'Total_Males'] + df.loc[16,'Total_Males']
    d['Males in Age not stated'] = df.loc[17, 'Total_Males']
#     d['Females in all ages'] = df.loc[0,'Total_Females']
    d['Females in Age 5-9'] = df.loc[1,'Total_Females']
    d['Females in Age 10-14'] = df.loc[2,'Total_Females']
    d['Females in Age 15-19'] = df.loc[3,'Total_Females']
    d['Females in Age 20-24'] = df.loc[4,'Total_Females']
    d['Females in Age 25-29'] = df.loc[5,'Total_Females']
    d['Females in Age 30-49'] = df.loc[6,'Total_Females'] + df.loc[7,'Total_Females'] + df.loc[8,'Total_Females'] + df.loc[9,'Total_Females'] 
    d['Females in Age 50-69'] = df.loc[10,'Total_Females'] + df.loc[11,'Total_Females'] + df.loc[12,'Total_Females'] + df.loc[13,'Total_Females']  
    d['Females in Age 70+']   = df.loc[14,'Total_Females'] + df.loc[15,'Total_Females'] + df.loc[16,'Total_Females']
    d['Females in Age not stated'] = df.loc[17, 'Total_Females']
    final = final.append(d, ignore_index=True)
final


# In[4]:


final_reserved = final.copy()


# # Reading language data

# In[5]:


# Reading Data for  third language from c-18
df = pd.read_excel('DDW-C18-0000.xlsx',engine='openpyxl')
df = df[1:]
df.columns = df.iloc[0]
df = df[1:]
df.columns = ['State_code','District_code','State_name','Rural/Urban','Age-group','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[3:]
df = df[(df['Age-group']!='Total')]
df = df[df['Rural/Urban']=='Total']
df.reset_index(drop=True,inplace=True)
df.head(10)


# # Part (a): 3+ language speaking 

# # Merging Language and Population data for each age group for each state/UT

# In[6]:


vals = set(df['Age-group'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Age-group']==i]
    t = t[['State_name','Males3','Females3']]
    t.columns = ['State_name','Males3+ in Age '+i,'Females3+ in Age '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
final


# In[7]:


final.columns


# # Finding ratio of Males and max age group for males

# In[8]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Age 5-9'] = final['Males3+ in Age 5-9']  / final['Males in Age 5-9']
final2['Age 10-14'] = final['Males3+ in Age 10-14']  / final['Males in Age 10-14']
final2['Age 15-19'] = final['Males3+ in Age 15-19']  / final['Males in Age 15-19']
final2['Age 20-24'] = final['Males3+ in Age 20-24']  / final['Males in Age 20-24']
final2['Age 25-29'] = final['Males3+ in Age 25-29']  / final['Males in Age 25-29']
final2['Age 30-49'] = final['Males3+ in Age 30-49']  / final['Males in Age 30-49']
final2['Age 50-69'] = final['Males3+ in Age 50-69']  / final['Males in Age 50-69']
final2['Age 70+'] = final['Males3+ in Age 70+']  / final['Males in Age 70+']
final2['Age not stated'] = final['Males3+ in Age Age not stated']  / final['Males in Age not stated']
final2
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Males max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Males max age group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Males max ratio','Males max age group']]
final2
table1 = final2.copy()


# # Finding ratio of Females and max age group for females

# In[9]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Age 5-9'] = final['Females3+ in Age 5-9']  / final['Females in Age 5-9']
final2['Age 10-14'] = final['Females3+ in Age 10-14']  / final['Females in Age 10-14']
final2['Age 15-19'] = final['Females3+ in Age 15-19']  / final['Females in Age 15-19']
final2['Age 20-24'] = final['Females3+ in Age 20-24']  / final['Females in Age 20-24']
final2['Age 25-29'] = final['Females3+ in Age 25-29']  / final['Females in Age 25-29']
final2['Age 30-49'] = final['Females3+ in Age 30-49']  / final['Females in Age 30-49']
final2['Age 50-69'] = final['Females3+ in Age 50-69']  / final['Females in Age 50-69']
final2['Age 70+'] = final['Females3+ in Age 70+']  / final['Females in Age 70+']
final2['Age not stated'] = final['Females3+ in Age Age not stated']  / final['Females in Age not stated']
final2
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Females max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Females max age group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Females max ratio','Females max age group']]
final2


# # Merging male and female outputs

# In[10]:


final2 = pd.concat([table1, final2],axis=1)
final2 = final2.loc[:,~final2.columns.duplicated()]
final2.columns = ['state/ut',  'ratio-males','age-group-males', 'ratio-females','age-group-females']
final2 = final2[['state/ut','age-group-males','ratio-males','age-group-females', 'ratio-females']]
final2


# # Writing ratio of 3 to csv

# In[11]:


final2.to_csv('./age-gender-a.csv',index=False)


# # Part (b): 2+ language speaking 

# # Merging Language and Population data for each age group for each state/UT

# In[12]:


final = final_reserved.copy()


# In[13]:


df.head(9)


# In[14]:


vals = set(df['Age-group'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Age-group']==i]
    t['Males2'] = t['Males2'] - t['Males3']
    t['Females2'] = t['Females2'] - t['Females3']
    t = t[['State_name','Males2','Females2']]
    t.columns = ['State_name','Males2+ in Age '+i,'Females2+ in Age '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
# final


# In[15]:


final.columns


# # Finding ratio of Males and max age group for males

# In[16]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Age 5-9'] = final['Males2+ in Age 5-9']  / final['Males in Age 5-9']
final2['Age 10-14'] = final['Males2+ in Age 10-14']  / final['Males in Age 10-14']
final2['Age 15-19'] = final['Males2+ in Age 15-19']  / final['Males in Age 15-19']
final2['Age 20-24'] = final['Males2+ in Age 20-24']  / final['Males in Age 20-24']
final2['Age 25-29'] = final['Males2+ in Age 25-29']  / final['Males in Age 25-29']
final2['Age 30-49'] = final['Males2+ in Age 30-49']  / final['Males in Age 30-49']
final2['Age 50-69'] = final['Males2+ in Age 50-69']  / final['Males in Age 50-69']
final2['Age 70+'] = final['Males2+ in Age 70+']  / final['Males in Age 70+']
final2['Age not stated'] = final['Males2+ in Age Age not stated']  / final['Males in Age not stated']

#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Males max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Males max age group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Males max ratio','Males max age group']]
table1 = final2.copy()


# # Finding ratio of Females and max age group for females

# In[17]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Age 5-9'] = final['Females2+ in Age 5-9']  / final['Females in Age 5-9']
final2['Age 10-14'] = final['Females2+ in Age 10-14']  / final['Females in Age 10-14']
final2['Age 15-19'] = final['Females2+ in Age 15-19']  / final['Females in Age 15-19']
final2['Age 20-24'] = final['Females2+ in Age 20-24']  / final['Females in Age 20-24']
final2['Age 25-29'] = final['Females2+ in Age 25-29']  / final['Females in Age 25-29']
final2['Age 30-49'] = final['Females2+ in Age 30-49']  / final['Females in Age 30-49']
final2['Age 50-69'] = final['Females2+ in Age 50-69']  / final['Females in Age 50-69']
final2['Age 70+'] = final['Females2+ in Age 70+']  / final['Females in Age 70+']
final2['Age not stated'] = final['Females2+ in Age Age not stated']  / final['Females in Age not stated']

#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Females max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Females max age group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Females max ratio','Females max age group']]
# final2


# # Merging male and female outputs

# In[18]:


final2 = pd.concat([table1, final2],axis=1)
final2 = final2.loc[:,~final2.columns.duplicated()]
final2.columns = ['state/ut',  'ratio-males','age-group-males', 'ratio-females','age-group-females']
final2 = final2[['state/ut','age-group-males','ratio-males','age-group-females', 'ratio-females']]
final2
final2


# # Writing ratio of 2 to csv

# In[19]:


final2.to_csv('./age-gender-b.csv',index=False)


# # Part (c): 1 language 

# # Merging Language and Population data for each age group for each state/UT

# In[20]:


final = final_reserved.copy()
final


# In[21]:


df


# In[22]:


vals = set(df['Age-group'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Age-group']==i]
    t = t[['State_name','Males2','Females2']]
    t.columns = ['State_name','Males1+ in Age '+i,'Females1+ in Age '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
final


# In[23]:


final.columns


# # Subtracting Total Population minus Population Speaking 2+ languages to get number of people speaking only 1 language

# In[24]:


final['Males1+ in Age 5-9'] = final['Males in Age 5-9'] - final['Males1+ in Age 5-9']
final['Males1+ in Age 10-14'] = final['Males in Age 10-14'] - final['Males1+ in Age 10-14']
final['Males1+ in Age 15-19'] = final['Males in Age 15-19'] - final['Males1+ in Age 15-19']
final['Males1+ in Age 20-24'] = final['Males in Age 20-24'] - final['Males1+ in Age 20-24']
final['Males1+ in Age 25-29'] = final['Males in Age 25-29'] - final['Males1+ in Age 25-29']
final['Males1+ in Age 30-49'] = final['Males in Age 30-49'] - final['Males1+ in Age 30-49']
final['Males1+ in Age 50-69'] = final['Males in Age 50-69'] - final['Males1+ in Age 50-69']
final['Males1+ in Age 70+'] = final['Males in Age 70+'] - final['Males1+ in Age 70+']
final['Males1+ in Age Age not stated'] = final['Males in Age not stated'] - final['Males1+ in Age Age not stated']
final['Females1+ in Age 5-9'] = final['Females in Age 5-9'] - final['Females1+ in Age 5-9']
final['Females1+ in Age 10-14'] = final['Females in Age 10-14'] - final['Females1+ in Age 10-14']
final['Females1+ in Age 15-19'] = final['Females in Age 15-19'] - final['Females1+ in Age 15-19']
final['Females1+ in Age 20-24'] = final['Females in Age 20-24'] - final['Females1+ in Age 20-24']
final['Females1+ in Age 25-29'] = final['Females in Age 25-29'] - final['Females1+ in Age 25-29']
final['Females1+ in Age 30-49'] = final['Females in Age 30-49'] - final['Females1+ in Age 30-49']
final['Females1+ in Age 50-69'] = final['Females in Age 50-69'] - final['Females1+ in Age 50-69']
final['Females1+ in Age 70+'] = final['Females in Age 70+'] - final['Females1+ in Age 70+']
final['Females1+ in Age Age not stated'] = final['Females in Age not stated'] - final['Females1+ in Age Age not stated']
final


# # Finding ratio of Males and max age group for males

# In[25]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Age 5-9'] = final['Males1+ in Age 5-9']  / final['Males in Age 5-9']
final2['Age 10-14'] = final['Males1+ in Age 10-14']  / final['Males in Age 10-14']
final2['Age 15-19'] = final['Males1+ in Age 15-19']  / final['Males in Age 15-19']
final2['Age 20-24'] = final['Males1+ in Age 20-24']  / final['Males in Age 20-24']
final2['Age 25-29'] = final['Males1+ in Age 25-29']  / final['Males in Age 25-29']
final2['Age 30-49'] = final['Males1+ in Age 30-49']  / final['Males in Age 30-49']
final2['Age 50-69'] = final['Males1+ in Age 50-69']  / final['Males in Age 50-69']
final2['Age 70+'] = final['Males1+ in Age 70+']  / final['Males in Age 70+']
final2['Age not stated'] = final['Males1+ in Age Age not stated']  / final['Males in Age not stated']

#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Males max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Males max age group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Males max ratio','Males max age group']]
table1 = final2.copy()


# # Finding ratio of Females and max age group for females

# In[26]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Age 5-9'] = final['Females1+ in Age 5-9']  / final['Females in Age 5-9']
final2['Age 10-14'] = final['Females1+ in Age 10-14']  / final['Females in Age 10-14']
final2['Age 15-19'] = final['Females1+ in Age 15-19']  / final['Females in Age 15-19']
final2['Age 20-24'] = final['Females1+ in Age 20-24']  / final['Females in Age 20-24']
final2['Age 25-29'] = final['Females1+ in Age 25-29']  / final['Females in Age 25-29']
final2['Age 30-49'] = final['Females1+ in Age 30-49']  / final['Females in Age 30-49']
final2['Age 50-69'] = final['Females1+ in Age 50-69']  / final['Females in Age 50-69']
final2['Age 70+'] = final['Females1+ in Age 70+']  / final['Females in Age 70+']
final2['Age not stated'] = final['Females1+ in Age Age not stated']  / final['Females in Age not stated']

#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Females max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Females max age group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Females max ratio','Females max age group']]
# final2


# # Merging male and female outputs

# In[27]:


final2 = pd.concat([table1, final2],axis=1)
final2 = final2.loc[:,~final2.columns.duplicated()]
final2.columns = ['state/ut',  'ratio-males','age-group-males', 'ratio-females','age-group-females']
final2 = final2[['state/ut','age-group-males','ratio-males','age-group-females', 'ratio-females']]
final2


# # Writing ratio of 1 to csv

# In[28]:


final2.to_csv('./age-gender-c.csv',index=False)


# In[29]:


print("Execution completed")

