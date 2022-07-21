#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[30]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings('ignore')


# # Reading Population of each literacy group for each state/UT

# In[31]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame()


# In[32]:


# Reading C-8 data
for i in range(0,36,1):
    # print(i)
    if(i<10):
        path = './c-8/DDW-0'+str(i)+'00C-08.xlsx'
    if(i>9):
        path = './c-8/DDW-'+str(i)+'00C-08.xlsx'
    df = pd.read_excel(path, engine='openpyxl')
    d = {}
    d['State_code'] = df.loc[6,'Unnamed: 1']
    d['Males Illiterate'] = df.loc[6,'Unnamed: 10']
    d['Males Literate'] = df.loc[6,'Unnamed: 13']
    d['Males Literate but below primary'] = df.loc[6,'Unnamed: 19']
    d['Males Primary but below middle'] = df.loc[6,'Unnamed: 22']
    d['Males Middle but below matric/secondary'] = df.loc[6,'Unnamed: 25']
    d['Males Matric/Secondary but below graduate'] = df.loc[6,'Unnamed: 28'] + df.loc[6,'Unnamed: 31'] + df.loc[6,'Unnamed: 34'] + df.loc[6,'Unnamed: 37'] 
    d['Males Graduate and above'] = df.loc[6,'Unnamed: 40']
    d['Females Illiterate'] = df.loc[6,'Unnamed: 11']
    d['Females Literate'] = df.loc[6,'Unnamed: 14']
    d['Females Literate but below primary'] = df.loc[6,'Unnamed: 20']
    d['Females Primary but below middle'] = df.loc[6,'Unnamed: 23']
    d['Females Middle but below matric/secondary'] = df.loc[6,'Unnamed: 26']
    d['Females Matric/Secondary but below graduate'] = df.loc[6,'Unnamed: 29'] + df.loc[6,'Unnamed: 32'] + df.loc[6,'Unnamed: 35'] + df.loc[6,'Unnamed: 38'] 
    d['Females Graduate and above'] = df.loc[6,'Unnamed: 41']  
    final = final.append(d, ignore_index=True)
final


# In[33]:


final_reserved = final.copy()


# # Reading Language Data

# In[34]:


# Reading Data for second and third language from C-19
df = pd.read_excel('./DDW-C19-0000.xlsx', engine='openpyxl')
df.columns = ['State_code','District_code','State_name','Rural/Urban','Educational level','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[(df['Rural/Urban']=='Total')&(df['Educational level']!='Total')]
df.reset_index(drop=True,inplace=True)
df


# # Part (a): 3+ languages

# # Merging Language and Literacy Data

# In[35]:


vals = set(df['Educational level'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Educational level']==i]
    t = t[['State_name','Males3','Females3']]
    t.columns = ['State_name','3+ lang Males in '+i,'3+ lang Females in '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
final


# In[36]:


final.columns


# # Finding ratio in different literary categories

# ## Males

# In[37]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Illiterate'] = final['3+ lang Males in Illiterate'] / final['Males Illiterate']
final2['Literate'] = final['3+ lang Males in Literate'] / final['Males Literate']
final2['Literate but below primary'] = final['3+ lang Males in Literate but below primary'] / final['Males Literate but below primary']
final2['Primary but below middle'] = final['3+ lang Males in Primary but below middle'] / final['Males Primary but below middle']
final2['Middle but below matric/secondary'] = final['3+ lang Males in Middle but below matric/secondary'] / final['Males Middle but below matric/secondary']
final2['Matric/Secondary but below graduate'] = final['3+ lang Males in Matric/Secondary but below graduate'] / final['Males Matric/Secondary but below graduate']
final2['Graduate and above'] = final['3+ lang Males in Graduate and above'] / final['Males Graduate and above']
# final2
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Males max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Males max literacy-group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Males max ratio','Males max literacy-group']]
table1 = final2.copy()
table1


# ## Females

# In[38]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Illiterate'] = final['3+ lang Females in Illiterate'] / final['Females Illiterate']
final2['Literate'] = final['3+ lang Females in Literate'] / final['Females Literate']
final2['Literate but below primary'] = final['3+ lang Females in Literate but below primary'] / final['Females Literate but below primary']
final2['Primary but below middle'] = final['3+ lang Females in Primary but below middle'] / final['Females Primary but below middle']
final2['Middle but below matric/secondary'] = final['3+ lang Females in Middle but below matric/secondary'] / final['Females Middle but below matric/secondary']
final2['Matric/Secondary but below graduate'] = final['3+ lang Females in Matric/Secondary but below graduate'] / final['Females Matric/Secondary but below graduate']
final2['Graduate and above'] = final['3+ lang Females in Graduate and above'] / final['Females Graduate and above']
# final2
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Females max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Females max literacy-group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Females max ratio','Females max literacy-group']]
table2 = final2.copy()
table2


# ## Merging

# In[39]:


final2 = pd.concat([table1, table2],axis=1)
final2 =final2.loc[:,~final2.columns.duplicated()]
final2


# In[40]:


final2.columns = ['state/ut','ratio-males','literacy-group-males','ratio-females','literacy-group-females']
final2 = final2[['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females']]
final2


# # Writing ratio of 3 languages to csv

# In[41]:


final2.to_csv('./literacy-gender-a.csv',index=False)


# # Part (b): 2 languages

# # Merging Language and Literacy Data

# In[42]:


final = final_reserved.copy()
vals = set(df['Educational level'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t['Males2'] = t['Males2'] - t['Males3']
    t['Females2'] = t['Females2'] - t['Females3']
    t = t[t['Educational level']==i]
    t = t[['State_name','Males2','Females2']]
    t.columns = ['State_name','2+ lang Males in '+i,'2+ lang Females in '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
final


# In[43]:


final.columns


# # Finding ratio in different literary categories

# ## Males

# In[44]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Illiterate'] = final['2+ lang Males in Illiterate'] / final['Males Illiterate']
final2['Literate'] = final['2+ lang Males in Literate'] / final['Males Literate']
final2['Literate but below primary'] = final['2+ lang Males in Literate but below primary'] / final['Males Literate but below primary']
final2['Primary but below middle'] = final['2+ lang Males in Primary but below middle'] / final['Males Primary but below middle']
final2['Middle but below matric/secondary'] = final['2+ lang Males in Middle but below matric/secondary'] / final['Males Middle but below matric/secondary']
final2['Matric/Secondary but below graduate'] = final['2+ lang Males in Matric/Secondary but below graduate'] / final['Males Matric/Secondary but below graduate']
final2['Graduate and above'] = final['2+ lang Males in Graduate and above'] / final['Males Graduate and above']
# final2
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Males max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Males max literacy-group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Males max ratio','Males max literacy-group']]
table1 = final2.copy()
table1


# ## Females

# In[45]:


final2 = pd.DataFrame()
final2['State_code'] = final['State_code']
final2['State_name'] = final['State_name']
final2['Illiterate'] = final['2+ lang Females in Illiterate'] / final['Females Illiterate']
final2['Literate'] = final['2+ lang Females in Literate'] / final['Females Literate']
final2['Literate but below primary'] = final['2+ lang Females in Literate but below primary'] / final['Females Literate but below primary']
final2['Primary but below middle'] = final['2+ lang Females in Primary but below middle'] / final['Females Primary but below middle']
final2['Middle but below matric/secondary'] = final['2+ lang Females in Middle but below matric/secondary'] / final['Females Middle but below matric/secondary']
final2['Matric/Secondary but below graduate'] = final['2+ lang Females in Matric/Secondary but below graduate'] / final['Females Matric/Secondary but below graduate']
final2['Graduate and above'] = final['2+ lang Females in Graduate and above'] / final['Females Graduate and above']
# final2
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Females max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Females max literacy-group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Females max ratio','Females max literacy-group']]
table2 = final2.copy()
table2


# ## Merging

# In[46]:


final2 = pd.concat([table1, table2],axis=1)
final2 =final2.loc[:,~final2.columns.duplicated()]
final2


# In[47]:


final2.columns = ['state/ut','ratio-males','literacy-group-males','ratio-females','literacy-group-females']
final2 = final2[['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females']]
final2


# # Writing ratio of 2 languages to csv

# In[48]:


final2.to_csv('./literacy-gender-b.csv',index=False)


# # Part (c): Exactly 1 language

# In[49]:


final = final_reserved.copy()
vals = set(df['Educational level'].unique())
for i in vals:
    t = pd.DataFrame()
    t = df.copy()
    t = t[t['Educational level']==i]
    t = t[['State_name','Males2','Females2']]
    t.columns = ['State_name','Males1+ in '+i,'Females1+ in '+i]
    t.reset_index(drop=True, inplace=True)
    final = pd.concat([final,t], axis=1)
final = final.loc[:,~final.columns.duplicated()]
final


# In[50]:


final.columns


# # Subtracting Total Population minus Population Speaking 2+ languages to get number of people speaking only 1 language

# In[51]:


final['Males1+ in Literate']                            = final['Males Literate'] - final['Males1+ in Literate'] 
final['Males1+ in Middle but below matric/secondary']   = final['Males Middle but below matric/secondary'] - final['Males1+ in Middle but below matric/secondary']
final['Males1+ in Matric/Secondary but below graduate'] = final['Males Matric/Secondary but below graduate'] - final['Males1+ in Matric/Secondary but below graduate']
final['Males1+ in Graduate and above']                  = final['Males Graduate and above'] - final['Males1+ in Graduate and above']
final['Males1+ in Primary but below middle']            = final['Males Primary but below middle'] - final['Males1+ in Primary but below middle']
final['Males1+ in Illiterate']                          = final['Males Illiterate'] - final['Males1+ in Illiterate']
final['Males1+ in Literate but below primary']          = final[ 'Males Literate but below primary'] - final['Males1+ in Literate but below primary']
final['Females1+ in Literate']                            = final['Females Literate'] - final['Females1+ in Literate'] 
final['Females1+ in Middle but below matric/secondary']   = final['Females Middle but below matric/secondary'] - final['Females1+ in Middle but below matric/secondary']
final['Females1+ in Matric/Secondary but below graduate'] = final['Females Matric/Secondary but below graduate'] - final['Females1+ in Matric/Secondary but below graduate']
final['Females1+ in Graduate and above']                  = final['Females Graduate and above'] - final['Females1+ in Graduate and above']
final['Females1+ in Primary but below middle']            = final['Females Primary but below middle'] - final['Females1+ in Primary but below middle']
final['Females1+ in Illiterate']                          = final['Females Illiterate'] - final['Females1+ in Illiterate']
final['Females1+ in Literate but below primary']          = final[ 'Females Literate but below primary'] - final['Females1+ in Literate but below primary']

final


# In[52]:


final.columns


# # Finding ratio of Males and max age group for males

# In[53]:


final2 = pd.DataFrame()
final2['State_code']  = final['State_code']
final2['State_name']  = final['State_name']
final2['Literate']                            = final['Males1+ in Literate']/final['Males Literate']  
final2['Middle but below matric/secondary']   = final['Males1+ in Middle but below matric/secondary']/final['Males Middle but below matric/secondary'] 
final2['Matric/Secondary but below graduate'] = final['Males1+ in Matric/Secondary but below graduate']/ final['Males Matric/Secondary but below graduate']
final2['Graduate and above']                  = final['Males1+ in Graduate and above']/final['Males Graduate and above']
final2['Primary but below middle']            = final['Males1+ in Primary but below middle']/ final['Males Primary but below middle']
final2['Illiterate']                          = final['Males1+ in Illiterate']/ final['Males Illiterate']
final2['Literate but below primary']          = final['Males1+ in Literate but below primary']/ final[ 'Males Literate but below primary']
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Males max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Males max literacy group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Males max ratio','Males max literacy group']]
table1 = final2.copy()
table1


# # Finding ratio of Females and max age group for females

# In[54]:


final2 = pd.DataFrame()
final2['State_code']  = final['State_code']
final2['State_name']  = final['State_name']
final2['Literate']                            = final['Females1+ in Literate']/final['Females Literate']  
final2['Middle but below matric/secondary']   = final['Females1+ in Middle but below matric/secondary']/final['Females Middle but below matric/secondary'] 
final2['Matric/Secondary but below graduate'] = final['Females1+ in Matric/Secondary but below graduate']/ final['Females Matric/Secondary but below graduate']
final2['Graduate and above']                  = final['Females1+ in Graduate and above']/final['Females Graduate and above']
final2['Primary but below middle']            = final['Females1+ in Primary but below middle']/ final['Females Primary but below middle']
final2['Illiterate']                          = final['Females1+ in Illiterate']/ final['Females Illiterate']
final2['Literate but below primary']          = final['Females1+ in Literate but below primary']/ final[ 'Females Literate but below primary']
#Finding maximum for each row and their column names
temp = final2.copy()
temp2 = final2.copy()
temp.drop(['State_code','State_name'],axis=1,inplace=True)
final2['Females max ratio'] = temp.max(axis=1)
temp2.drop(['State_code','State_name'],axis=1,inplace=True)
temp2 = temp2.astype('float64')
final2['Females max literacy group'] = temp2.idxmax(axis=1, skipna=True)
final2 = final2[['State_code','Females max ratio','Females max literacy group']]
table2 = final2.copy()
table2


# # Merging male and female outputs

# In[55]:


final2 = pd.concat([table1, table2],axis=1)
final2 = final2.loc[:,~final2.columns.duplicated()]
final2


# In[56]:


final2.columns = ['state/ut','ratio-males','literacy-group-males','ratio-females','literacy-group-females']
final2 = final2[['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females']]
final2


# # Writing ratio of 1 languages to csv

# In[57]:


final2.to_csv('./literacy-gender-c.csv',index=False)


# In[58]:


print("Execution completed")


# In[ ]:




