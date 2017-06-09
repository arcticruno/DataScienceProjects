import pandas as pd
import numpy as np

# atp_data = pd.read_csv("C:/Users/onur.seker/workspace/atp/tennis_atp_master/atp_data_set.csv", low_memory = False)
#  
#   
# #remove all data, that has no matchstats
# atp_data = atp_data.dropna(axis = 0, subset = ["w_ace"])
# #reset index
# atp_data = atp_data.reset_index()
# #rename unnamed to number and round to tourney_round
# atp_data.rename(columns = {'Unnamed: 0' : 'number'}, inplace = True)
# atp_data.rename(columns = {'round' : 't_round'}, inplace = True)
# print(atp_data.keys())
#     
# #pickle data
# atp_data.to_pickle("C:/Users/onur.seker/workspace/atp/tennis_atp_master/atp_data_set.pickle")

atp_data = pd.read_pickle("C:/Users/onur.seker/workspace/atp/tennis_atp_master/atp_data_set.pickle")
print(atp_data.keys())

print('')


#create a data_set without DavisCup
atp_data = atp_data[atp_data.tourney_level != 'D']
print(atp_data.tourney_level.unique())

#Check how many unique categories are in the data
for col_name in atp_data.columns:
    if atp_data[col_name].dtype == 'object':
        unique_cat = len(atp_data[col_name].unique())
        print("Feature:'{col_name}' has {unique_cat} unique categories".format(col_name = col_name, unique_cat = unique_cat))

#print(atp_data.loc[(atp_data['tourney_name']=='Roland Garros') & (atp_data['tourney_date']==20160523), 'tourney_date'].count())

