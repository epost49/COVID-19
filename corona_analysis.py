#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:02:59 2020

@author: ethan
"""

# This script plots COVID-19 time series data.
# The data comes from a Johns Hopkins GitHub repo.
# The goal is to identify trends in the reported deaths and to quantify the spread.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os
import datetime as dt

def get_country_total(df, country_label, states=None):
    # This function takes in a pandas DataFrame and a "Country/Region" label to
    # produce a list of dates and a list of country totals, packaged in a 
    # dictionary. The DataFrame comes from a csv file in a particular format.
    df = pd.read_csv(fpath)  # extract DataFrame from csv file
    date_list = df.columns.values.tolist()[4:]  # convert DataFrame header to a list, and remove first 4 elements
    formatted_dates = [dt.datetime.strptime(d,"%m/%d/%y").date() for d in date_list]
    country_rows = df.loc[df['Country/Region'] == country_label]  # extract rows for desired country
    if states:
        country_rows = country_rows.loc[us_rows['Province/State'].isin(states)]  # extract rows with state names
        
    country_rows2 = country_rows.drop(['Province/State','Country/Region','Lat','Long'],axis=1)  # remove unwanted columns
    country_row_tot = country_rows2.apply(np.sum,axis=0)  # sum all the country values
    country_tot_list = country_row_tot.values.tolist()  # convert DataFrame to a list
    out = {'dates':formatted_dates, 'country_total':country_tot_list}
    
    return out
    

datadir = "/home/ethan/Documents/Code/COVID-19/input_data"
date_dir = "2020-03-19"
fpath = os.path.join(datadir, date_dir, "time_series_19-covid-Deaths.csv")

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

#us_data = []
#with open(fpath) as csvfile:
#    csvreader = csv.reader(csvfile, delimiter=',')
#    header = next(csvreader)
#    for row in csvreader:
#        if row[0] == "California":
#            ca_data = row[4:]
#        if (row[0] in states) and (row[1] == "US"):
#            us_data.append(row[4:])
            
df = pd.read_csv(fpath)  # extract DataFrame from csv file
date_list = df.columns.values.tolist()[4:]  # convert DataFrame header to a list, and remove first 4 elements
formatted_dates = [dt.datetime.strptime(d,"%m/%d/%y").date() for d in date_list]
us_rows = df.loc[df['Country/Region'] == 'US']  # extract US rows
us_rows = us_rows.loc[us_rows['Province/State'].isin(states)]  # extract rows with state names
us_rows2 = us_rows.drop(['Province/State','Country/Region','Lat','Long'],axis=1)  # remove unwanted columns
us_row_tot = us_rows2.apply(np.sum,axis=0)  # sum all the US values
us_tot_list = us_row_tot.values.tolist()  # convert DataFrame to a list

plt.figure(1)
plt.plot(formatted_dates, us_tot_list)
plt.xticks(rotation=45)
plt.tight_layout()
plt.figure(2)
plt.semilogy(formatted_dates, us_tot_list)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#us_matrix = np.array(us_data)
#us_total = np.sum(us_matrix, axis=0)

#dates = header[4:]
#formatted_dates = [dt.datetime.strptime(d,"%m/%d/%y").date() for d in dates]

#plt.plot(formatted_dates, ca_data)
#plt.plot(formatted_dates, us_total)
#plt.show()
        
