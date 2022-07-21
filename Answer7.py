#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np
import openpyxl
import warnings as ws
ws.filterwarnings('ignore')


# In[24]:


col_names = [
 'State_code',
 'State_name',
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']


# In[25]:


# Data Frame containing all details for all States/UTs
final_a = pd.DataFrame(columns=col_names) #Using mother tongue
final_b = pd.DataFrame(columns=col_names) #Using mother tongue +2nd +3rd language


# In[26]:


# Reading c-17 data
for i in range(1,36,1):
    # print(i)
    if(i<10):
        path = './c-17/DDW-C17-0'+str(i)+'00.XLSX'
    if(i>9):
        path = './c-17/DDW-C17-'+str(i)+'00.XLSX'
    df = pd.read_excel(path, engine='openpyxl')
    df.columns = ['State_code','State_name','Language1 code','Language1 Name','Population1','Males1','Females1','Language2 code','Language2 Name','Population2','Males2','Females2','Language3 code','Language3 Name','Population3','Males3','Females3']
    df = df[5:]
    df.fillna(0,inplace=True)
    df = df[['State_code','State_name','Language1 code','Language1 Name','Population1','Language2 code','Language2 Name','Population2','Language3 code','Language3 Name','Population3']]
    df.reset_index(drop=True, inplace=True)
    
    d = {}
    d['State_code'] = df.loc[0,'State_code']
    d['State_name'] = df.loc[0,'State_name']

    df1 = df.copy()
    df1 = df[df['Language1 code']!=0]
    df1 = df1[['Language1 code','Language1 Name','Population1']]
    df1 = df1.groupby(['Language1 code','Language1 Name'])[['Population1']].agg(sum)
    df1['Language1 Name'] = df1.index.to_numpy()
    df1['Language1 Name'] = df1['Language1 Name'].apply(lambda x: x[1])
    df1['Language1 code'] = df1.index.to_numpy()
    df1['Language1 code'] = df1['Language1 code'].apply(lambda x: x[0])
    df1.reset_index(drop=True, inplace=True)
    dict1 = pd.Series(df1.Population1.values,index=df1['Language1 code']+'_'+df1['Language1 Name']).to_dict()
#     print("Dictionary1:\n",dict1)
    dict_temp = dict1.copy()
    dict_temp.update(d)
    final_a = final_a.append(dict_temp,ignore_index=True)
    
    df2 = df.copy()
    df2 = df2[df2['Language2 code']!=0]
    df2 = df2[['Language2 code','Language2 Name','Population2']]
    df2 = df2.groupby(['Language2 code','Language2 Name'])[['Population2']].agg(sum)
    df2['Language2 Name'] = df2.index.to_numpy()
    df2['Language2 Name'] = df2['Language2 Name'].apply(lambda x: x[1])
    df2['Language2 code'] = df2.index.to_numpy()
    df2['Language2 code'] = df2['Language2 code'].apply(lambda x: x[0])
    df2.reset_index(drop=True, inplace=True)
    dict2 = pd.Series(df2.Population2.values,index=df2['Language2 code']+'_'+df2['Language2 Name']).to_dict()
#     print("Dictionary2:\n",dict2)

    df3 = df.copy()
    df3 = df3[df3['Language3 code']!=0]
    df3 = df3[['Language3 code','Language3 Name','Population3']]
    df3 = df3.groupby(['Language3 code','Language3 Name'])[['Population3']].agg(sum)
    df3['Language3 Name'] = df3.index.to_numpy()
    df3['Language3 Name'] = df3['Language3 Name'].apply(lambda x: x[1])
    df3['Language3 code'] = df3.index.to_numpy()
    df3['Language3 code'] = df3['Language3 code'].apply(lambda x: x[0])
    df3.reset_index(drop=True, inplace=True)
    dict3 = pd.Series(df3.Population3.values,index=df3['Language3 code']+'_'+df3['Language3 Name']).to_dict()
#     print("Dictionary3:\n",dict3)

#     print("Dictionary0:\n",d)

    # Merging 3 temporary dictionaries
    c = {x: dict1.get(x, 0) + dict2.get(x, 0) for x in set(dict1).union(dict2)}
    c = {x: c.get(x, 0) + dict3.get(x, 0) for x in set(c).union(dict3)}
    c.update(d)

    final_b = final_b.append(c, ignore_index = True)# final


# In[27]:


final_a


# In[28]:


final_b


# ## Filling Nan with 0 as the langugaes not present in a particular state data are not spoken at all in that state

# In[29]:


final_a.fillna(0, inplace=True)
final_b.fillna(0, inplace=True)


# In[30]:


final_b.isna().sum(),final_b.isna().sum()


# ## Reordering the columns for better view

# In[31]:


final_a = final_a[[
 'State_code',
 'State_name',
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']]
final_a


# In[32]:


final_b = final_b[[
 'State_code',
 'State_name',
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']]
final_b


# # Adding regions for each state/UT

# In[33]:


# Adding regions North South etc to dataframe
def region( i ):
    if (i=='01' or i=='02' or i=='03' or i=='04' or i=='05' or i=='06' or i=='07' ):
        return 'North'
    if (i=='08' or i=='24' or i=='27' or i=='25' or i=='26' or i=='30' ):
        return 'West'
    if (i=='09' or i=='22' or i=='23' ):
        return 'Central'
    if (i=='10' or i=='19' or i=='20' or i=='21' ):
        return 'East'
    if (i=='28' or i=='29' or i=='33' or i=='32' or i=='31' or i=='34' ):
        return 'South'
    return 'North-East'
final_a['region'] = final_a['State_code'].map(region)
final_b['region'] = final_b['State_code'].map(region)


# ## Reordering the columns for simplification of view

# In[34]:


final_a = final_a[[
 'State_code',
 'State_name',
  'region',
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']]
final_a


# In[35]:


final_b = final_b[[
 'State_code',
 'State_name',
  'region',
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']]
final_b


# In[36]:


# Dropping state code and state names
final_a = final_a.drop(['State_code','State_name'],axis=1)
final_b = final_b.drop(['State_code','State_name'],axis=1)


# # Merging the dataframe by regions

# In[37]:


final2a = final_a.copy()
final2a = final2a.groupby('region')[[
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']].apply(sum)
final2a['region'] = final2a.index.to_numpy()
final2a.reset_index(drop=True, inplace=True)
final2a


# In[38]:


final2b = final_b.copy()
final2b = final2b.groupby('region')[[
 '001000_ASSAMESE',
 '002000_BENGALI ',
 '003000_BODO ',
 '004000_DOGRI ',
 '005000_GUJARATI',
 '006000_HINDI ',
 '007000_KANNADA',
 '008000_KASHMIRI ',
 '009000_KONKANI',
 '010000_MAITHILI ',
 '011000_MALAYALAM',
 '012000_MANIPURI ',
 '013000_MARATHI ',
 '014000_NEPALI ',
 '015000_ODIA ',
 '016000_PUNJABI ',
 '017000_SANSKRIT ',
 '018000_SANTALI ',
 '019000_SINDHI',
 '020000_TAMIL ',
 '021000_TELUGU ',
 '022000_URDU',
 '023000_ADI ',
 '024000_AFGHANI/KABULI/PASHTO ',
 '025000_ANAL ',
 '026000_ANGAMI ',
 '027000_AO ',
 '028000_ARABIC/ARBI ',
 '029000_BALTI ',
 '030000_BHILI/BHILODI ',
 '031000_BHOTIA ',
 '032000_BHUMIJ ',
 '033000_BISHNUPURIYA',
 '034000_CHAKHESANG ',
 '035000_CHAKRU/CHOKRI ',
 '036000_CHANG ',
 '037000_COORGI/KODAGU ',
 '038000_DEORI ',
 '039000_DIMASA ',
 '040000_ENGLISH ',
 '041000_GADABA ',
 '042000_GANGTE ',
 '043000_GARO ',
 '044000_GONDI',
 '045000_HALABI',
 '046000_HALAM ',
 '047000_HMAR',
 '048000_HO',
 '049000_JATAPU ',
 '050000_JUANG ',
 '051000_KABUI ',
 '052000_KARBI/MIKIR ',
 '053000_KHANDESHI',
 '054000_KHARIA ',
 '055000_KHASI ',
 '056000_KHEZHA ',
 '057000_KHIEMNUNGAN',
 '058000_KHOND/KONDH ',
 '059000_KINNAURI ',
 '060000_KISAN ',
 '061000_KOCH ',
 '062000_KODA/KORA ',
 '063000_KOLAMI ',
 '064000_KOM',
 '065000_KONDA',
 '066000_KONYAK ',
 '067000_KORKU ',
 '068000_KORWA ',
 '069000_KOYA ',
 '070000_KUI ',
 '071000_KUKI',
 '072000_KURUKH/ORAON ',
 '073000_LADAKHI ',
 '074000_LAHAULI ',
 '075000_LAHNDA ',
 '076000_LAKHER',
 '077000_LALUNG ',
 '078000_LEPCHA ',
 '079000_LIANGMEI ',
 '080000_LIMBU ',
 '081000_LOTHA ',
 '082000_LUSHAI/MIZO ',
 '083000_MALTO ',
 '084000_MAO',
 '085000_MARAM',
 '086000_MARING ',
 '087000_MIRI/MISHING',
 '088000_MISHMI ',
 '089000_MOGH ',
 '090000_MONPA ',
 '091000_MUNDA',
 '092000_MUNDARI ',
 '093000_NICOBARESE ',
 '094000_NISSI/DAFLA ',
 '095000_NOCTE ',
 '096000_PAITE',
 '097000_PARJI ',
 '098000_PAWI ',
 '100000_PHOM ',
 '101000_POCHURY',
 '102000_RABHA ',
 '103000_RAI ',
 '104000_RENGMA ',
 '105000_SANGTAM ',
 '106000_SAVARA',
 '107000_SEMA',
 '108000_SHERPA ',
 '109000_SHINA',
 '111000_TAMANG ',
 '112000_TANGKHUL ',
 '113000_TANGSA',
 '114000_THADO ',
 '115000_TIBETAN ',
 '116000_TRIPURI ',
 '117000_TULU ',
 '118000_VAIPHEI ',
 '119000_WANCHO',
 '120000_YIMCHUNGRE',
 '121000_ZELIANG ',
 '122000_ZEMI ',
 '123000_ZOU ',
 '124000_OTHERS']].apply(sum)
final2b['region'] = final2b.index.to_numpy()
final2b.reset_index(drop=True, inplace=True)
final2b


# # Part (a) : Mother tongue only

# In[39]:


final3a = final2a.T
final3a.columns = final3a.iloc[len(final3a)-1]
final3a.drop(final3a.tail(1).index,inplace=True)
final3a


# In[40]:


ans = pd.DataFrame()
final3a['Central'] = final3a['Central'].astype('int64')
ans['Central'] = final3a.nlargest(3,'Central')['Central'].index

final3a['East'] = final3a['East'].astype('int64')
ans['East'] = final3a.nlargest(3,'East')['East'].index

final3a['North'] = final3a['North'].astype('int64')
ans['North'] = final3a.nlargest(3,'North')['North'].index

final3a['North-East'] = final3a['North-East'].astype('int64')
ans['North-East'] = final3a.nlargest(3,'North-East')['North-East'].index

final3a['West'] = final3a['West'].astype('int64')
ans['West'] = final3a.nlargest(3,'West')['West'].index

final3a['South'] = final3a['South'].astype('int64')
ans['South'] = final3a.nlargest(3,'South')['South'].index
ans = ans.T
ans['region'] = ans.index
ans.columns = ['language-1','language-2','language-3','region'] 
ans = ans[['region','language-1','language-2','language-3']]
ans.reset_index(drop=True,inplace=True)
ans['language-1'] = ans['language-1'].apply(lambda x: x.split('_')[1])
ans['language-2'] = ans['language-2'].apply(lambda x: x.split('_')[1])
ans['language-3'] = ans['language-3'].apply(lambda x: x.split('_')[1])
ans.sort_values('region', inplace = True)
ans


# # Writing output to csv file

# In[41]:


ans.to_csv('./region-india-a.csv', index=False)


# # Part(b) : Mother tongue + 2nd language + 3rd language

# In[42]:


final3b = final2b.T
final3b.columns = final3b.iloc[len(final3b)-1]
final3b.drop(final3b.tail(1).index,inplace=True)
final3b


# In[43]:


ans = pd.DataFrame()
final3b['Central'] = final3b['Central'].astype('int64')
ans['Central'] = final3b.nlargest(3,'Central')['Central'].index

final3b['East'] = final3b['East'].astype('int64')
ans['East'] = final3b.nlargest(3,'East')['East'].index

final3b['North'] = final3b['North'].astype('int64')
ans['North'] = final3b.nlargest(3,'North')['North'].index

final3b['North-East'] = final3b['North-East'].astype('int64')
ans['North-East'] = final3b.nlargest(3,'North-East')['North-East'].index

final3b['West'] = final3b['West'].astype('int64')
ans['West'] = final3b.nlargest(3,'West')['West'].index

final3b['South'] = final3b['South'].astype('int64')
ans['South'] = final3b.nlargest(3,'South')['South'].index
ans = ans.T
ans['region'] = ans.index
ans.columns = ['language-1','language-2','language-3','region'] 
ans = ans[['region','language-1','language-2','language-3']]
ans.reset_index(drop=True,inplace=True)
ans['language-1'] = ans['language-1'].apply(lambda x: x.split('_')[1])
ans['language-2'] = ans['language-2'].apply(lambda x: x.split('_')[1])
ans['language-3'] = ans['language-3'].apply(lambda x: x.split('_')[1])
ans.sort_values('region', inplace = True)
ans


# # Writing output to csv file

# In[44]:


ans.to_csv('./region-india-b.csv',index=False)


# In[ ]:




