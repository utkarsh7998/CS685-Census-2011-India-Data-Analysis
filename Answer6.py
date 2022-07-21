#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[1]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings("ignore")


# # Reading Population of each literacy group for each state/UT

# In[2]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame(columns=['State_code', 'Illiterate', 'Literate','Literate but below primary', 'Primary but below middle','Middle but below matric/secondary','Matric/Secondary but below graduate','Graduate and above'])


# In[ ]:


# Reading c-8 data
for i in range(0,36,1):
    # print(i)
    if(i<10):
        path = './c-8/DDW-0'+str(i)+'00C-08.xlsx'
    if(i>9):
        path = './c-8/DDW-'+str(i)+'00C-08.xlsx'
    df = pd.read_excel(path, engine='openpyxl')
    d = {}
    d['State_code'] = df.loc[6,'Unnamed: 1']
    d['Illiterate'] = df.loc[6,'Unnamed: 9']
    d['Literate'] = df.loc[6,'Unnamed: 12']
    d['Literate but below primary'] = df.loc[6,'Unnamed: 18']
    d['Primary but below middle'] = df.loc[6,'Unnamed: 21']
    d['Middle but below matric/secondary'] = df.loc[6,'Unnamed: 24']
    d['Matric/Secondary but below graduate'] = df.loc[6,'Unnamed: 27'] + df.loc[6,'Unnamed: 30'] + df.loc[6,'Unnamed: 33'] + df.loc[6,'Unnamed: 36'] 
    d['Graduate and above'] = df.loc[6,'Unnamed: 39']  
    final = final.append(d, ignore_index=True)
final


# # Reading Language Data

# In[ ]:


# Reading Data for second and third language from c-18
df = pd.read_excel('./DDW-C19-0000.xlsx', engine='openpyxl')
df.columns = ['State_code','District_code','State_name','Rural/Urban','Educational level','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[(df['Rural/Urban']=='Total')&(df['Educational level']!='Total')]
df.reset_index(drop=True,inplace=True)
df


# # Merging Language and Literacy Data

# In[ ]:


vals = set(df['Educational level'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Educational level']==i]
    t = t[['State_name','Number speaking third language']]
    t.columns = ['State_name','3+ lang in '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
# final.columns=['State_code', 'State_name','Graduate and above', 'Illiterate', 'Literate','Matric/Secondary but below graduate',
#        'Middle but below matric/secondary', 'Primary but below middle','Literate but below primary', '3+ lang in Literate but below primary',
#        '3+ lang in Primary but below middle', '3+ lang in Graduate and above','3+ lang in Middle but below matric/secondary', '3+ lang in Literate',
#        '3+ lang in Illiterate','3+ lang in Matric/Secondary but below graduate']


# In[ ]:


final


# # Finding percentage in different literary categories

# In[ ]:


final2 = final.copy()


# In[ ]:


final2['percent Illiterate'] = (final2['3+ lang in Illiterate']*100)/final2['Illiterate']
final2['percent Literate'] = (final2['3+ lang in Literate']*100)/final2['Literate']
final2['percent Literate but below primary'] = (final2['3+ lang in Literate but below primary']*100)/final2['Literate but below primary']
final2['percent Primary but below middle'] = (final2['3+ lang in Primary but below middle']*100)/final2['Primary but below middle']
final2['percent Middle but below matric/secondary'] = (final2['3+ lang in Middle but below matric/secondary']*100)/final2['Middle but below matric/secondary']
final2['percent Matric/Secondary but below graduate'] = (final2['3+ lang in Matric/Secondary but below graduate']*100)/final2['Matric/Secondary but below graduate']
final2['percent Graduate and above'] = (final2['3+ lang in Graduate and above']*100)/final2['Graduate and above']
# final2['percent 70+'] = (final2['3+ lang in 70+']*100)/final2['Age 70+']
# final2['percent Age not stated'] = (final2['3+ lang in Age not stated']*100)/final2['Age not stated']
final2 = final2[['State_code','State_name','percent Illiterate','percent Literate','percent Literate but below primary','percent Primary but below middle','percent Middle but below matric/secondary','percent Matric/Secondary but below graduate','percent Graduate and above']]
final2


# In[ ]:


#Changing column names
final2.columns = ['State_code', 'State_name','Illiterate', 'Literate', 'Literate but below primary',
       'Primary but below middle', 'Middle but below matric/secondary',
       'Matric/Secondary but below graduate', 'Graduate and above']


# # Finding maximum literacy group in each state/UT

# In[ ]:


#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['percentage'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['literacy-group'] = temp2.idxmax(axis=1, skipna=True)
final2


# In[ ]:


ans = final2.copy()
ans = ans[['State_code','literacy-group','percentage']]
ans.columns = ['state/ut','literacy-group','percentage']
ans


# # Writing output to csv

# In[ ]:


ans.to_csv('./literacy-india.csv', index=False)


# In[ ]:


print("Execution completed")

