# -*- coding: utf-8 -*-
"""
This script reads in the data provided by Boston regarding neighborhood
data on: age, education, nativity, race, labor, and housing demographics for
all Boston neighborhoods. 

Each neighborhood is on a different sheet within a .xlsx file. We need to 
  read in all the data, 
  separate by demographic variable,
  and union all neighborhoods into the variable dataframe.


Created on Wed Oct 14 11:49:17 2020
@author: cwhaley
"""

import pandas as pd

# used in create_demographics_function to turn off ".iloc" error when referencing rows
pd.options.mode.chained_assignment = None  # default='warn'


df_dict = pd.read_excel(input("Enter filepath: "), sheet_name=None)  # read in all sheets


# list of neighborhoods
df_dict.keys()


#define different data groups
age = ['0-9 years', '10-19 years', '20-34 years', '35-54 years', '55-64 years', '65 years and over']
education = ['less than High School', 'High School or GED', "Some College or Associate's Degree", "Bachelor's Degree or Higher"]
nativity = ['Foreign Born']
race = ['White', 'Black/ African American', 'Hispanic', 'Asian/PI', 'Other']
labor = ['Male', 'Female']
housing = ['Occupied Housing Units', 'Owner-occupied', 'Renter-occupied']



# take variable list to pull applicable rows from dataframes in dict, union dataframes into one
def create_demographic_dataframes(dictionary, demographic_variable, demo_col_name):
  df2 = pd.DataFrame()
  #loop through dict to pull out dataframe rows based on demographic_variable
  for key, value in dictionary.items():
     df = value[value.iloc[:,0].isin(demographic_variable)]     # rows based on demographic variable
     df = df.iloc[:,0:8]                                        # columns = category, populations in years
     df['neighborhood'] = key                                   # add the neighborhood name to rows
     df2 = pd.concat([df, df2], 0)                              # union dataframes together
  # add column names
  df2.columns = [demo_col_name, '1950', '1960', '1970', '1980', '1990', '2000', '2010', 'neighborhood']
  # reshape from wide to long
  df2 = (df2.set_index(['neighborhood', str(demo_col_name)])
       .stack()
       .reset_index(name='a')
       .rename(columns={'level_2':'year', 'a':'population'}))
  return df2
  

#==================================================================================
# Demographic Data Tables
#==================================================================================
# pull rows for demographic data, union all neighborhoods into one dataframe
age_df = create_demographic_dataframes(df_dict, age, 'age')
edu_df = create_demographic_dataframes(df_dict, education, 'education_attainment')
nativity_df = create_demographic_dataframes(df_dict, nativity, 'nativity')
race_df = create_demographic_dataframes(df_dict, race, 'race')
labor_df = create_demographic_dataframes(df_dict, labor, 'labor')
housing_df = create_demographic_dataframes(df_dict, housing, 'housing')


