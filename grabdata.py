import numpy as np
import pandas as pd

#Read Data
macro = "/Users/Onur/Documents/workspace/sberbank/macro.csv"
test = "/Users/Onur/Documents/workspace/sberbank/test.csv"
train = "/Users/Onur/Documents/workspace/sberbank/train.csv"

test = pd.read_csv(test)
train = pd.read_csv(train)
macro = pd.read_csv(macro)
#Merge test with macro on timestamp 
complete = pd.merge(train, macro, on = ["timestamp"])

header_train = list(train.columns)
header_test = list(test.columns)
header_macro = list(macro.columns)
header_complete = list(complete.columns)

#make price_doc last
price_doc = header_complete[291]
del header_complete[291]
header_complete.append(price_doc)
complete = complete[header_complete]
complete_shape = complete.shape


#Summary statistics:
typesdictionary = dict(complete.dtypes)
dummy = []
for i in range(len(header_complete)):
    if 'object' == typesdictionary[header_complete[i]]:
        dummy.append(header_complete[i])
    else:
        pass


dummy
print(dummy)