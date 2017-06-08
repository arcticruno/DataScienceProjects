import pandas as pd
import numpy as np

#name directory 
directory = "C:/Users/onur.seker/workspace/tennis_atp-master/"

#create a list with all the csvnames
variable_list = ["atp_matches_{}.csv".format(date) for date in range(1968,2017+1,1)]

#merge directory name with csvnames
for i in range(len(variable_list)):
    variable_list[i] = directory+variable_list[i]

atp_matches_1968 = pd.read_csv(variable_list[0])
atp_matches_1969 = pd.read_csv(variable_list[1])
atp_matches_1970 = pd.read_csv(variable_list[2])
atp_matches_1971 = pd.read_csv(variable_list[3])
atp_matches_1972 = pd.read_csv(variable_list[4])
atp_matches_1973 = pd.read_csv(variable_list[5])
atp_matches_1974 = pd.read_csv(variable_list[6])
atp_matches_1975 = pd.read_csv(variable_list[7])
atp_matches_1976 = pd.read_csv(variable_list[8])
atp_matches_1977 = pd.read_csv(variable_list[9])
atp_matches_1978 = pd.read_csv(variable_list[10])
atp_matches_1979 = pd.read_csv(variable_list[11])
atp_matches_1980 = pd.read_csv(variable_list[12])
atp_matches_1981 = pd.read_csv(variable_list[13])
atp_matches_1982 = pd.read_csv(variable_list[14])
atp_matches_1983 = pd.read_csv(variable_list[15])
atp_matches_1984 = pd.read_csv(variable_list[16])
atp_matches_1985 = pd.read_csv(variable_list[17])
atp_matches_1986 = pd.read_csv(variable_list[18])
atp_matches_1987 = pd.read_csv(variable_list[19])
atp_matches_1988 = pd.read_csv(variable_list[20])
atp_matches_1989 = pd.read_csv(variable_list[21])
atp_matches_1990 = pd.read_csv(variable_list[22])
atp_matches_1991 = pd.read_csv(variable_list[23])
atp_matches_1992 = pd.read_csv(variable_list[24])
atp_matches_1993 = pd.read_csv(variable_list[25])
atp_matches_1994 = pd.read_csv(variable_list[26])
atp_matches_1995 = pd.read_csv(variable_list[27])
atp_matches_1996 = pd.read_csv(variable_list[28])
atp_matches_1997 = pd.read_csv(variable_list[29])
atp_matches_1998 = pd.read_csv(variable_list[30])
atp_matches_1999 = pd.read_csv(variable_list[31])
atp_matches_2000 = pd.read_csv(variable_list[32])
atp_matches_2001 = pd.read_csv(variable_list[33])
atp_matches_2002 = pd.read_csv(variable_list[34])
atp_matches_2003 = pd.read_csv(variable_list[35])
atp_matches_2004 = pd.read_csv(variable_list[36])
atp_matches_2005 = pd.read_csv(variable_list[37])
atp_matches_2006 = pd.read_csv(variable_list[38])
atp_matches_2007 = pd.read_csv(variable_list[39])
atp_matches_2008 = pd.read_csv(variable_list[40])
atp_matches_2009 = pd.read_csv(variable_list[41])
atp_matches_2010 = pd.read_csv(variable_list[42])
atp_matches_2011 = pd.read_csv(variable_list[43])
atp_matches_2012 = pd.read_csv(variable_list[44])
atp_matches_2013 = pd.read_csv(variable_list[45])
atp_matches_2014 = pd.read_csv(variable_list[46])
atp_matches_2015 = pd.read_csv(variable_list[47])
atp_matches_2016 = pd.read_csv(variable_list[48])
atp_matches_2017 = pd.read_csv(variable_list[49])

#create frames for concatenating into one large dataset
frames = [atp_matches_1968,atp_matches_1969,
          atp_matches_1970,atp_matches_1971,atp_matches_1972,atp_matches_1973,atp_matches_1974,
          atp_matches_1975,atp_matches_1976,atp_matches_1977,atp_matches_1978,atp_matches_1979,
          atp_matches_1980,atp_matches_1981,atp_matches_1982,atp_matches_1983,atp_matches_1984,
          atp_matches_1985,atp_matches_1986,atp_matches_1987,atp_matches_1988,atp_matches_1989,
          atp_matches_1990,atp_matches_1991,atp_matches_1992,atp_matches_1993,atp_matches_1994,
          atp_matches_1995,atp_matches_1996,atp_matches_1997,atp_matches_1998,atp_matches_1999,
          atp_matches_2000,atp_matches_2001,atp_matches_2002,atp_matches_2003,atp_matches_2004,
          atp_matches_2005,atp_matches_2006,atp_matches_2007,atp_matches_2008,atp_matches_2009,
          atp_matches_2010,atp_matches_2011,atp_matches_2012,atp_matches_2013,atp_matches_2014,
          atp_matches_2015,atp_matches_2016,atp_matches_2017]

#create a large data_set
atp_data_set = pd.concat(frames)

#output the data set as a csv file
atp_data_set.to_csv("C:/Users/onur.seker/workspace/tennis_atp-master/atp_data_set.csv", encoding = "utf-8")

