import pandas as pd
import numpy as np
import pickle
import re

#===============================================================================
# SETUP
#===============================================================================

#Load directory
path = "C:/Users/onur.seker/workspace/MallOfAmerica/mall_raw.xlsx"

#Set up excelfile as pandas dataframe
xl = pd.ExcelFile(path)

#===============================================================================
# DATAWRANGLING
#===============================================================================



#===============================================================================
# FRIT
#===============================================================================

#get dataframe from excel sheet
FRIT = xl.parse('FRIT')

#rename columns
FRIT.rename(columns = {'Property, City, State, Zip Code':"name_and_location", 'Year Completed':"year_built", 
                       "Year Acquired":"year_acquired", "Square Feet(1) /Apartment Units":"GLA", 
                       "Average Rent Per Square Foot(2)":"rent_per_sq", "Percentage Leased(3)":"pct_lease",
                        "Principal Tenant(s)":"tenants"}, inplace = True)



#Regex to find only the ','in order to separate Name from location
#Create a zipcode container
zipcodes = r'\,'

#Create a boolean by zipcode container
names_bool = FRIT.name_and_location.str.contains(zipcodes)
#print(names_bool)
#Create new variable with property names only
property_location = FRIT.name_and_location.ix[names_bool == True]
property_names = FRIT.name_and_location.ix[names_bool == False]


#Align indexes
property_location.index = property_names.index
#Add property name and location
FRIT['name_and_location'] = property_names
FRIT.rename(columns = {"name_and_location":"property_name"}, inplace = True)
FRIT['property_location'] = property_location

#Datensatz
FRIT.property_location.fillna(method = 'ffill', inplace = True)
FRIT.property_name.fillna(method = 'ffill', inplace = True)
cols = ['property_name', 'state', 'city', 'zipcode','legal_ownersh']
 
#Regex to get city
city = r'(\,?)'
FRIT['city'] = FRIT.property_location.str.split(city).str.get(0)
#print(FRIT.head())

#remove numbers in bracket
state_and_zip = FRIT.property_location.str.split(city).str.get(2)
bracket_remove = r'\(?'
state_and_zip = state_and_zip.str.split(bracket_remove).str.get(0)
  
#split by state and zip
split = r'\s'
FRIT['state'] = state_and_zip.str.split(split).str.get(1)
FRIT['zipcode'] = state_and_zip.str.split(split).str.get(2)
del FRIT['property_location']

FRIT.pct_lease = FRIT.pct_lease*100
# print(len(FRIT['Tenants']))
# print(len(FRIT['pct_lease']))


#===============================================================================
# Create function that assigns tenants in different rows to its property_name 
#===============================================================================

#get all tenants in each property as a list works only after forwardfill property names

def compriment_rows(property_name,tenant,data):
    tenant_list =[]
    for i in data['{}'.format(property_name)]:
        tenant_list.append(list(data['{}'.format(tenant)][data['{}'.format(property_name)] == i]))
    data['{}'.format(tenant)] = pd.Series(tenant_list)


compriment_rows('property_name','tenants',FRIT)
#Drop all duplicates subsetting by property_names
FRIT = FRIT.drop_duplicates(subset = "property_name")
#print(FRIT.head())
FRIT['REIT'] = 'FRIT'




#===============================================================================
# SGP  
#===============================================================================
#get SGP from excelsheet
SGP = xl.parse('SGP')

#rename
SGP.rename(columns = {'U.S. Properties':"ID", 'Unnamed: 1':'property_name', 
                       "Unnamed: 2":"blank", "Unnamed: 3":"state", 
                       "Unnamed: 4":"blank", "Unnamed: 5":"city",
                        "Unnamed: 6":"blank", "Unnamed: 7":"ownership_interest", 
                        "Unnamed: 8":"blank", "Unnamed: 9":"ownership",
                        "Unnamed: 10":"percent", "Unnamed: 11":"year_built_acquired", "Unnamed: 12":"blank",
                        "Unnamed: 13":"pct_lease", "Unnamed: 14":"percentage", "Unnamed: 15":"GLA",
                        "Unnamed: 16":"blank", "Unnamed: 17":"tenants"}, inplace = True)
   
#Drop all blanks
SGP.drop(SGP['blank'], axis = 1, inplace = True)
 
#Drop first 9 rows
SGP = SGP[9:]
SGP = SGP[1:]
del SGP['ID']
del SGP['percent']
del SGP['ownership_interest']
del SGP['percentage']
#Reset Index
SGP.reset_index(drop = True, inplace = True)
SGP.fillna(method = 'ffill', inplace = True)

#clean property names
bracket_remove = r'(\s\()'

SGP.property_name = SGP.property_name.str.split(bracket_remove).str.get(0)


#print
#change built to completed
splitter = r'\s'
SGP['owner_status'] = SGP.year_built_acquired.str.split(splitter, expand = True)[0]
SGP['owner_status_year'] = SGP.year_built_acquired.str.split(splitter, expand = True)[1]
del SGP['year_built_acquired']

SGP['year_built'] = SGP.owner_status_year[(SGP.owner_status == 'Built')]
SGP['year_acquired'] = SGP.owner_status_year[(SGP.owner_status == 'Acquired')]
del SGP['owner_status']
del SGP['owner_status_year']

compriment_rows('property_name','tenants',SGP)


#Drop duplicates
SGP = SGP.drop_duplicates(subset = "property_name")

SGP['REIT'] = 'SGP'

#===============================================================================
# Kimco
#===============================================================================

Kimco = xl.parse('Kimco')


Kimco.state.fillna(method = 'ffill', inplace = True)


#Replace States with state abbreviation

state_abbreviations = {"alabama":"AL", "alaska":"AK", "arizona":"AZ", "arkansas":"AR",
                       "california":"CA", "colorado":"CO", "connecticut":"CT","delaware":"DE",
                       "florida":"FL", "georgia":"GA", "hawaii":"HI", "idaho":"ID", "illinois":"IL",
                       "indiana":"IN", "iowa":"IA", "kansas":"KS", "kentucky":"KY", "louisiana":"LA",
                       "maine":"ME", "maryland":"MD", "massachusetts":"MA", "michigan":"MI", "minnesota":"MN",
                       "mississippi":"MS", "missouri":"MO", "montana":"MT", "nebraska":"NE", "nevada":"NV",
                       "new hampshire":"NH", "new jersey":"NJ", "new mexico":"NM", "new york":"NY",
                       "north carolina":"NC", "north dakota":"ND", "ohio":"OH", "oklahoma":"OK", "oregon":"OR",
                       "pennsylvania":"PA", "rhode island":"RI", "south carolina":"SC", "south dakota":"SD",
                       "tennessee":"TN","texas":"TX", "utah":"UT", "vermont":"VT", "virginia":"VA", "washington":"WA",
                       "west virginia":"WV", "wisconsin":"WI", "wyoming":"WY", "puerto rico":"PR"} 


lowercase_states = [Kimco.state[i].lower() for i in range(Kimco.state.shape[0])]
states = [state_abbreviations[state] for state in lowercase_states]
Kimco.state = pd.Series(states)

#Drop NA columns
Kimco.dropna(thresh = 11, inplace = True)

#Drop Kimco              
Kimco = Kimco.dropna(subset = ["major_tenant1", "major_tenant2", "Grocery_tenant"], how = 'all' )


bracket_remove = r'(\s\()'
Kimco.city = Kimco.city.str.split(bracket_remove).str.get(0)


Kimco.Grocery_tenant = Kimco.Grocery_tenant.str.split(bracket_remove).str.get(0)

#set length
rows = Kimco.shape[0]
Kimco.reset_index(drop = True, inplace = True)

#create new list with tenants in each mall in one column
tenants = [[list(Kimco.major_tenant1)[i], list(Kimco.major_tenant2)[i], list(Kimco.Grocery_tenant)[i]] for i in range(rows)]
Kimco["tenants"] = pd.Series(tenants)

Kimco = Kimco[["state", "city", "Developed_or_aacquired", "sq_feet", "pct_lease", "tenants"]]
Kimco.rename(columns = {"Developed_or_aacquired": "year_built_or_acquired", "sq_feet":"GLA"}, inplace = True)


Kimco['REIT'] = 'Kimco'


#===============================================================================
# WPG
#===============================================================================


WPG = xl.parse("WPG")




WPG.rename(columns = {'Property Name':"property_name", "State":"state", 'sq_feet': 'GLA',
                      "City (Major Metropolitan Area)":"city",
                        "Financial":"ownership", "Year":"year", "Occupancy (%)(2)":"pct_lease", "Anchors":"tenants"}, inplace = True)


WPG.property_name.fillna(method = 'ffill', inplace = True)

compriment_rows("property_name", "tenants", WPG)

WPG = WPG.drop_duplicates(subset = "property_name")
WPG['owner_status'] = WPG.year.str.split(splitter, expand = True)[0]
WPG['owner_status_year'] = WPG.year.str.split(splitter, expand = True)[1]
del WPG['year']
WPG['year_built'] = WPG.owner_status_year[(WPG.owner_status == 'Built')]
WPG['year_acquired'] = WPG.owner_status_year[(WPG.owner_status == 'Acquired')]
del WPG['owner_status']
del WPG['owner_status_year']
del WPG['Ownership']
WPG['REIT'] = 'WPG'

#===============================================================================
# MACERICH
#===============================================================================


MACE = xl.parse("MACERICH")


#Create new variable with property names only
property_name = MACE.property_name[::2].str.split(r'\(').str.get(0)
property_location = MACE.property_name[1::2]

#align indexes
property_location.index = property_name.index


#Add property name and location
MACE['property_location'] = property_location
MACE['property_name'] = property_name

#Split State and city
MACE['city'] = MACE.property_location.str.split(r'\,').str.get(0)
MACE['state'] = MACE.property_location.str.split(r'\, ').str.get(1)
del MACE['property_location']


#Split construction_year and acquisition

MACE['year_built'] = MACE.year.str.split(r'\/').str.get(0)
MACE['year_acquired'] = MACE.year.str.split(r'\/').str.get(1)
del MACE['year']


#State Abbreviation
MACE.state.fillna(method = 'ffill', inplace = True)
lowercase_states = [MACE.state[i].lower() for i in range(MACE.state.shape[0])]
states = [state_abbreviations[state] for state in lowercase_states]
MACE.state = pd.Series(states)

#ownership
MACE.ownership = MACE.ownership.str.split(r'\%').str.get(0)
#delete blank column
del MACE['Unnamed: 10']
del MACE['Count']

#rename
MACE.rename(columns = {'Non-Owned Anchors (3)':'tenants_non_owned', 'Company-Owned Anchors (3)':'tenants_owned',
                       'sq_feet':'GLA'}, inplace = True)
MACE.property_name.fillna(method = 'ffill', inplace = True)
compriment_rows('property_name','tenants_non_owned',MACE)
compriment_rows('property_name', 'tenants_owned', MACE)
MACE['tenants'] = MACE['tenants_non_owned'] + MACE['tenants_owned']
MACE = MACE.drop_duplicates(subset = "property_name")
del MACE['tenants_non_owned']
del MACE['tenants_owned']
MACE['REIT'] = 'MACE'



#===============================================================================
# GGP
#===============================================================================
GGP = xl.parse('GGP')

GGP.property_name = GGP.property_name.str.split(r' \(').str.get(0)

GGP['city'] = GGP.location.str.split(r'\,').str.get(0)
GGP['state'] = GGP.location.str.split(r'\, ').str.get(1)
del GGP['location']
del GGP['ID']
GGP.rename(columns = {'sq_feet':'GLA', 'mall_freestanding_GLA':'free_GLA'}, inplace = True)
GGP.property_name.fillna(method = 'ffill', inplace = True)

compriment_rows('property_name','tenants',GGP)
GGP = GGP.drop_duplicates(subset = "property_name")
GGP['REIT'] = 'GGP'

#===============================================================================
# PREIT
#===============================================================================

PREIT = xl.parse('PREIT')



names_bool = PREIT.property_name.str.contains(r'\,\Z')

property_location = PREIT.property_name.ix[names_bool == False]
property_names = PREIT.property_name.ix[names_bool == True]

property_names = property_names.str.split(r'\,').str.get(0)


#Align indexes
property_location.index = property_names.index



#Add property name and location
PREIT['property_name'] = property_names
PREIT['property_location'] = property_location


#Datensatz
PREIT.property_location.fillna(method = 'ffill', inplace = True)
PREIT.property_name.fillna(method = 'ffill', inplace = True)
  
   
#Regex to get city
city = r'\,'
PREIT['city'] = PREIT.property_location.str.split(city).str.get(0)
PREIT['state'] = PREIT.property_location.str.split(city).str.get(1)
bracket_remove = r'\(?'
PREIT['state'] = PREIT.state.str.split(bracket_remove).str.get(0)
del PREIT['property_location']


PREIT['year_built'] = PREIT['year_built/last_renovation'].str.split(r'\/').str.get(0)
PREIT['last_renovation'] = PREIT['year_built/last_renovation'].str.split(r'\/').str.get(1)



compriment_rows('property_name','tenants',PREIT)
PREIT = PREIT.drop_duplicates(subset = "property_name")
PREIT['REIT'] = 'PREIT'
PREIT.rename(columns = {'Interest':'ownership', 'sq_feet':'GLA'}, inplace = True)

PREIT['ownership'] = PREIT['ownership']*100
PREIT['pct_lease'] = PREIT['pct_lease']*100
del PREIT['year_built/last_renovation']
del PREIT['owned_sq_feet']



#===============================================================================
# CBL
#===============================================================================

CBL = xl.parse('CBL')

names_bool = CBL.property_name.str.contains(r'[^A-Z]\Z')
property_location = CBL.property_name.ix[names_bool == False]
property_names = CBL.property_name.ix[names_bool == True]
property_location.index = property_names.index



city = r'\,'
CBL['property_name'] = property_names
CBL['city'] = property_location.str.split(city).str.get(0).str.strip()
CBL['state'] = property_location.str.split(city).str.get(1)
CBL = CBL.dropna(how = 'all')
CBL['REIT'] = 'CBL'
CBL = CBL.dropna(thresh = 10)

CBL['year_built'] = CBL['year_built/acquisition'].str.split(r'\/').str.get(0)
CBL['year_acquired'] = CBL['year_built/acquisition'].str.split(r'\/').str.get(1)
del CBL['year_built/acquisition']
del CBL['mall_store_sales_p_sq_foot']
CBL.rename(columns = {'latest_renovation':'last_renovation', 'sq_feet':'GLA', 'GLA':"free_GLA"},inplace = True)

CBL.ownership = CBL.ownership*100
CBL.pct_lease = CBL.pct_lease*100

CBL.tenants = CBL.tenants.str.split('\,')


#===============================================================================
# 
#===============================================================================


result = FRIT.append([SGP, Kimco, WPG, GGP, PREIT, CBL, MACE])

result.reset_index(drop = True, inplace = True)


print(result.GLA.type())





#result.to_csv("C:/Users/onur.seker/workspace/MallOfAmerica/malls.csv")


























