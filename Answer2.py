#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings("ignore")


# # Reading Total Population, No. of Males, No. of females for each state/UT

# In[13]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame()
# columns=['State_code','State_name','Population']


# In[14]:


# Reading C-17 data
for i in range(0,36,1):
    if(i<10):
        path = './c-17/DDW-C17-0'+str(i)+'00.XLSX'
    if(i>9):
        path = './c-17/DDW-C17-'+str(i)+'00.XLSX'
    df = pd.read_excel(path, engine='openpyxl')
    df = df[1:]
    df.columns = df.iloc[0]
    df = df[1:]
    df.columns = ['State_code','State_name','Total speakers of languages','Name','Population1','Males1','Females1','Number of speakers speaking subsidiary languages (1st language)','1 st subsidiary languages','Population2','Males2','Females2','Number of speakers speaking subsidiary languages (2nd language)','2nd subsidiary languages','Population3','Males3','Females3']
    df = df[3:]
    df = df[['State_code','State_name','Total speakers of languages','Population1', 'Males1','Females1','Population2', 'Males2','Females2','Population3', 'Males3','Females3']]
    df.reset_index(drop=True,inplace=True)
    df.fillna(0,inplace=True)
    d = {}
    d['State_code'] = df.loc[0,'State_code']
    d['State_name'] = df.loc[0,'State_name']
    d['Total_Males'] = df['Males1'].sum()
    d['Total_Females'] = df['Females1'].sum()
    final = final.append(d, ignore_index = True)
final


# # Reading no of males and females speaking 3 or more language for each state/UT

# In[15]:


# Reading Data for second and third language from c-18
df = pd.read_excel('DDW-C18-0000.xlsx',engine='openpyxl')
df = df[1:]
df.columns = df.iloc[0]
df = df[1:]
df.columns = ['State_code','District_code','State_name','Rural/Urban','Age-group','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[3:]
df = df[(df['Rural/Urban']=='Total')&(df['Age-group']=='Total')]
df = df.drop(['District_code','Rural/Urban','Age-group'],axis='columns')
df = df[['State_code','State_name','Females2','Males2','Females3','Males3']]
df.reset_index(drop=True,inplace=True)
df


# # Concatenating Population and Language Dataframe

# In[16]:


# Concatenating c-17 and c-18 data
final2 = pd.concat([final, df],axis=1)

# Dropping duplicate columns formed after concatenation
final2 = final2.loc[:,~final2.columns.duplicated()]
final2


# # Subtracting Total Males - Males2 to get Males1

# In[17]:


final2['Males1'] = (final2['Total_Males'] - final2['Males2']).astype('int')
final2['Females1'] = (final2['Total_Females'] - final2['Females2']).astype('int')
final2['Males2'] = (final2['Males2'] - final2['Males3']).astype('int')
final2['Females2'] = (final2['Females2'] - final2['Females3']).astype('int')
final2


# # Statistical test and p-value reporting

# In[18]:


# Making answer dataframe
ans = final2.copy()
ans['Ratio1'] = ans['Males1']/ans['Females1']
ans['Ratio2'] = ans['Males2']/ans['Females2']
ans['Ratio3'] = ans['Males3']/ans['Females3']
ans['Ratio'] = ans['Total_Males'] / ans['Total_Females']
ans['pvalue'] = -1

from scipy.stats import ttest_1samp
for i in range(len(ans)):
    temp = ttest_1samp(a = [ans.loc[i,'Ratio1'],ans.loc[i,'Ratio2'],ans.loc[i,'Ratio3']], popmean=ans.loc[i,'Ratio'])
    ans.loc[i,'pvalue'] = temp[1]
ans['Males1'] = (ans['Males1']/ans['Total_Males'])*100
ans['Males2'] = (ans['Males2']/ans['Total_Males'])*100
ans['Males3'] = (ans['Males3']/ans['Total_Males'])*100
ans['Females1'] = (ans['Females1']/ans['Total_Females'])*100
ans['Females2'] = (ans['Females2']/ans['Total_Females'])*100
ans['Females3'] = (ans['Females3']/ans['Total_Females'])*100
ans = ans[['State_code','Males1','Males2','Males3','Females1','Females2','Females3','pvalue']]
ans.columns = ['state-code','male-percentage-1','male-percentage-2','male-percentage-3','female-percentage-1','female-percentage-2','female-percentage-3','p-value']
ans


# In[19]:


part1 = ans.copy()
part2 = ans.copy()
part3 = ans.copy()
part1 = part1[['state-code','male-percentage-1','female-percentage-1','p-value']]
part1.columns = ['state-code','male-percentage','female-percentage','p-value']
part2 = part2[['state-code','male-percentage-2','female-percentage-2','p-value']]
part2.columns = ['state-code','male-percentage','female-percentage','p-value']
part3 = part3[['state-code','male-percentage-3','female-percentage-3','p-value']]
part3.columns = ['state-code','male-percentage','female-percentage','p-value']


# In[20]:


part1


# # Writing output to csv file

# In[21]:


part1.to_csv('./gender-india-a.csv',index=False)
part2.to_csv('./gender-india-b.csv',index=False)
part3.to_csv('./gender-india-c.csv',index=False)


# In[22]:


print("Execution completed")


# In[ ]:




