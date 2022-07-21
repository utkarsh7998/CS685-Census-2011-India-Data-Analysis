#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[1]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings("ignore")


# # Reading Urban and Rural Population Data

# In[2]:


# Data Frame containing all details for all States/UTs
final = pd.DataFrame()


# In[3]:


# Reading Population Data
df = pd.read_excel("./c-14/DDW-0000C-14.xls")
df.columns = ['Table_name','State_code','Dist_code','State_Name','Age-group','Total_Persons','Total_Males','Total_Females','Rural Population','Rural_Males','Rural_Females','Urban Population','Urban_Males','Urban_Females']
df = df[6:]
df = df[df['Dist_code']=='000']
df.reset_index(drop=True,inplace=True)
df.fillna(0,inplace=True)    
df = df[(df['Age-group']=='All ages')]
df = df[['State_code','Urban Population','Rural Population']]
final =df.copy()
final.reset_index(drop=True, inplace=True)
final


# # Reading population data for 
# ## (i) people speaking 2 languages, 3 or more languages in Rural areas
# ## (ii) people speaking 2 languages,3 or more languages in Urban areas

# In[4]:


# Reading Data for third language from c-18
df = pd.read_excel('DDW-C18-0000.xlsx',engine='openpyxl')
df = df[1:]
df.columns = df.iloc[0]
df = df[1:]
df.columns = ['State_code','District_code','State_name','Rural/Urban','Age-group','Number speaking second language','Males2','Females2','Number speaking third language','Males3','Females3']
df = df[3:]
# df = df[df['State_name']!='INDIA']
df = df[((df['Rural/Urban']=='Rural')|(df['Rural/Urban']=='Urban'))&(df['Age-group']=='Total')]
df.reset_index(drop=True,inplace=True)
df


# In[5]:


#Taking out rural population and urban population for each state
df1 = df.copy()
df2 = df.copy()
df1 = df1[df1['Rural/Urban']=='Rural']
df2 = df2[df2['Rural/Urban']=='Urban']
df1 = df1[['State_code','State_name','Number speaking second language','Number speaking third language']]
df1.columns= ['State_code','State_name','Rural2','Rural3']
df1.reset_index(drop=True, inplace=True)
# df1
df2 = df2[['State_code','State_name','Number speaking second language','Number speaking third language']]
df2.columns= ['State_code','State_name','Urban2','Urban3']
df2.reset_index(drop=True, inplace=True)
# df2
df3 = pd.concat([df1,df2],axis=1)
df3 = df3.loc[:,~df3.columns.duplicated()]
df = df3.copy()
df


# # Concatenating population and language dataframes

# In[6]:


# Concatenating c-17 and c-18 data
final2 = pd.concat([final, df],axis=1)

# Dropping duplicate columns formed after concatenation
final2 = final2.loc[:,~final2.columns.duplicated()]
final2


# # Finding number  of  people
# ## (i) rural population speaking exactly 1 and exactly 2 languages
# ## (ii) urban population speaking exactly 1 and exactly 2 languages

# In[7]:


# Making answer dataframe
ans = final2.copy()
ans['Rural1'] = ans['Rural Population'] - ans['Rural2']
ans['Urban1'] = ans['Urban Population'] - ans['Urban2']
ans['Rural2'] = ans['Rural2'] - ans['Rural3']
ans['Urban2'] = ans['Urban2'] - ans['Urban3']
final2 = ans.copy()
final2
                                                                                        


# # Statistical test and p-value reporting

# In[8]:


# Making answer dataframe
ans = final2.copy()
ans['Ratio1'] = ans['Urban1']/ans['Rural1']
ans['Ratio2'] = ans['Urban2']/ans['Rural2']
ans['Ratio3'] = ans['Urban3']/ans['Rural3']
ans['Ratio'] = ans['Urban Population']/ans['Rural Population']
ans['pvalue'] = -1

from scipy.stats import ttest_1samp
for i in range(len(ans)):
    temp = ttest_1samp(a = [ans.loc[i,'Ratio1'],ans.loc[i,'Ratio2'],ans.loc[i,'Ratio3']], popmean=ans.loc[i,'Ratio'])
    ans.loc[i,'pvalue'] = temp[1]
ans['Rural1'] = (ans['Rural1']/ans['Rural Population'])*100
ans['Rural2'] = (ans['Rural2']/ans['Rural Population'])*100
ans['Rural3'] = (ans['Rural3']/ans['Rural Population'])*100
ans['Urban1'] = (ans['Urban1']/ans['Urban Population'])*100
ans['Urban2'] = (ans['Urban2']/ans['Urban Population'])*100
ans['Urban3'] = (ans['Urban3']/ans['Urban Population'])*100
ans = ans[['State_code','Rural1','Rural2','Rural3','Urban1','Urban2','Urban3','pvalue']]
ans.columns = ['state-code','rural-percentage-1','rural-percentage-2','rural-percentage-3','urban-percentage-1','urban-percentage-2','urban-percentage-3','p-value']
ans


# In[9]:


part1 = ans.copy()
part2 = ans.copy()
part3 = ans.copy()
part1 = part1[['state-code','urban-percentage-1','rural-percentage-1','p-value']]
part1.columns = ['state-code','urban-percentage','rural-percentage','p-value']
part2 = part2[['state-code','urban-percentage-2','rural-percentage-2','p-value']]
part2.columns = ['state-code','urban-percentage','rural-percentage','p-value']
part3 = part3[['state-code','urban-percentage-3','rural-percentage-3','p-value']]
part3.columns = ['state-code','urban-percentage','rural-percentage','p-value']


# In[10]:


part1


# # Writing output to csv file

# In[11]:


part1.to_csv('./geography-india-a.csv',index=False)
part2.to_csv('./geography-india-b.csv',index=False)
part3.to_csv('./geography-india-c.csv',index=False)


# In[12]:


print("Execution completed")


# In[ ]:




