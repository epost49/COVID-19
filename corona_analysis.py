#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:02:59 2020

@author: Ethan
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
        country_rows = country_rows.loc[country_rows['Province/State'].isin(states)]  # extract rows with state names
        
    country_rows2 = country_rows.drop(['Province/State','Country/Region','Lat','Long'],axis=1)  # remove unwanted columns
    country_row_tot = country_rows2.apply(np.sum,axis=0)  # sum all the country values
    country_tot_list = country_row_tot.values.tolist()  # convert DataFrame to a list
    out = {'dates':formatted_dates, 'country_total':country_tot_list}
    
    return out
    
def plot_figs(x, y, country_label):

    fig, ((ax1), (ax2)) = plt.subplots(nrows=2, sharex=True)

    ax1.plot(x, y, 'r')
    ax1.set(ylabel='Death Count')

    ax2.semilogy(x, y, 'b')
    ax2.set(ylabel='Death Count')
    plt.xticks(rotation=45)
    fig.suptitle('COVID-19 deaths (' + country_label + ')',y=0.95)
    plt.tight_layout()
    plt.show()

def plot_figs2(x,y,country_label,fign,y_max):
    
    f, axarr = plt.subplots(2,1, sharex=True)
    axarr[0].plot(x, y)
    axarr[0].set_title('COVID-19 deaths per million (' + country_label + ')')
    axarr[0].grid(True, axis='y')
    axarr[1].semilogy(x, y)
    axarr[1].set_ylim(.001, y_max)
    axarr[1].grid(True, axis='y')
    
    for tick in axarr[1].get_xticklabels():
        tick.set_rotation(55)
    
    plt.tight_layout()
    plt.figure(fign)


datadir = "/home/ethan/Documents/Code/COVID-19/input_data"
date_dir = "2020-03-19"
fpath = os.path.join(datadir, date_dir, "time_series_19-covid-Deaths.csv")

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

#countries = ['US','Italy']
country_dict = [{'country':'US','states':states,'population':327000000},
                {'country':'Canada','states':None,'population':37600000},
                {'country':'Italy','states':None,'population':60500000}]

df = pd.read_csv(fpath)  # extract DataFrame from csv file

y_max = 1000

i = 1
for c in country_dict:
    data_lists = get_country_total(df, c['country'], c['states'])  # get dictionary of time list and country total list
    x = data_lists['dates']
    y = data_lists['country_total']
    y_arr = np.array(y)
    y_arr = np.multiply(np.divide(y_arr,c['population']),1000000)  # deaths per million
    y = list(y_arr)
    start_index = 20
    plot_figs2(x[start_index:], y[start_index:], c['country'],i,y_max)
    i = i + 1

#data_lists = get_country_total(df, 'US', states)  # get dictionary of time list and country total list
#x = data_lists['dates']
#y = data_lists['country_total']
#
#start_index = 40
#plot_figs2(x[start_index:], y[start_index:], 'US',1)
#plot_figs2(x[start_index:], y[start_index:], 'Italy',2)
plt.show()

