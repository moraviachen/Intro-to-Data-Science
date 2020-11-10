import pandas as pd 
import numpy as np
import json
import sys

sys.path.insert(1,'../data')

df = pd.read_csv("../data/nyc_311_limit.csv")
### CLEAN DATA COLUMN
cols = [str(i) for i in range(0, len(df.columns))]
df.columns = cols
date_df = df[['1','2','8']].copy()
date_df = date_df[date_df['8'].notna()]
date_df['8'] = date_df['8'].astype('Int64')
### GET DIFFERENCE 
date_df['1'] = pd.to_datetime(date_df['1'], format="%m/%d/%Y %I:%M:%S %p") 
date_df['2'] = pd.to_datetime(date_df['2'], format="%m/%d/%Y %I:%M:%S %p")
date_df['difference'] = date_df['2'] - date_df['1']
date_df['hours'] = date_df['difference'] / np.timedelta64(1, 'h')
date_df = date_df[date_df['hours'] >= 0]
### MONTH COLUMN 
date_df['month'] = pd.DatetimeIndex(date_df['2']).month
### COUNTER COLUMN 
date_df['counter'] = 1
print(date_df)

sum_df = date_df.groupby(['8', 'month']).agg({'hours': 'sum', 'counter': 'sum'}).reset_index()
### Total Average Response Time 
total_df = date_df.groupby(['month']).agg({'hours': 'sum', 'counter': 'sum'}).reset_index()
total_df['hourPerCounter'] = total_df['hours'] / total_df['counter']
total_df = total_df[['month', 'hourPerCounter']]
total_df.to_csv("../data/total.csv")
### Sum of zipline average Response Time 
sum_df['hourPerCounter'] = sum_df['hours'] / sum_df['counter']
sum_df = sum_df[['8', 'month', 'hourPerCounter']]
newf = sum_df.pivot(index='8', columns='month')
newf.columns = newf.columns.droplevel(0)
newf.to_csv("../data/ziplineAverage.csv")





