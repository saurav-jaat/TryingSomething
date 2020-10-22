#!/usr/bin/env python
# coding: utf-8

# ---
# # Add education features to the training file
# 1.`has_common_schools`
# 
# 2.`n_common_schools`

# In[1]:


# Loading Libraries
import pandas as pd
import numpy as np
from tabulate import tabulate

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split as ttsplit

import constants

RANDOM_STATE = constants.RANDOM_STATE


# In[2]:


# Loading training data
df_train = pd.read_csv(constants.OUTPUT_FILE)
print(df_train.shape)
df_train.head()


# ## Loading Lookup dataFrame
# 

# In[3]:


# Loading skills table to create a lookup to create feature from
df_schools = pd.read_csv(constants.DATA_PATH+'user_educations.csv')
df_schools.head()


# In[4]:


# dropping duplicates
df_schools.drop_duplicates(inplace=True)


# In[5]:


# Grouping the schools by user_id
df_schools_grouped = df_schools.groupby('user_id')


# In[6]:


# Accessing the schools of particular user
df_schools_grouped.get_group(151)


# In[7]:


# Utility function to lookup values in 
def get_common_info(userA, userB, df_info, var):
    """
    Lookup group of info for userA and userB
    
    `df_info` can be replaced by `df_school` or any other which conveys extra
    about `userA` or `userB` BUT MUST BE GROUPED BY `user_id`
    
    
    Returns
        has_common_info: boolean: whether the users have common school
        n_common_info: int: count of schools common between the users
    """
    userA = int(userA)
    userB = int(userB)
    #
    # try block if no info is present
    try:
        # feteching skills 
        uA_info = set(df_info.get_group(userA)[var].values)
        uB_info = set(df_info.get_group(userB)[var].values)
        commons = uA_info.intersection(uB_info)
        #
        # if info has only 999999 (i.e. the group of less freq info); DEFINED BY PROBLEM STATEMENT
        if ( 999999 in commons) and (len(commons - {999999, }) <1):
            return True, -2
        # else find the common info expect
        n_common_info = len( commons-{999999, })
        has_common_info = True if n_common_info > 0 else False
    # when no school information is present
    except Exception as e:
        return False, -1
    return has_common_info, n_common_info

# Testing the function
# get_common_schools(151, 931, df_skills_grouped, var='skill_id')
# get_common_schools(51, 5371)
# get_common_schools(151, 41)


# ### Creating features

# In[8]:


# Generating Features
temp = df_train.apply(lambda x: get_common_info(x.userA_id, x.userB_id, df_schools_grouped, var='school_id'),
                  axis=1)
temp = np.array(temp.to_list())
df_train['has_common_schools'] = temp[:, 0] 
df_train['n_common_schools'] = temp[:, 1]


# In[9]:


# Preview of new features
df_train.head()


# --- 
# Writing to file
# ---

# In[10]:


# Writing to output
df_train.to_csv(constants.OUTPUT_FILE,
                index=False,
                header=True)

