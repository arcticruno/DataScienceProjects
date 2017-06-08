import pandas as pd
import numpy as np


atp_data = pd.read_csv("C:/Users/onur.seker/workspace/tennis_atp-master/atp_data_set.csv", low_memory = False)

#remove all data, that has no matchstats
atp_data = atp_data.dropna(axis = 0, subset = ["w_ace"])
#reset index
atp_data = atp_data.reset_index()
#rename unnamed to count
atp_data.rename(columns = {'Unnamed: 0' : 'number'}, inplace = True)
print(atp_data.keys())