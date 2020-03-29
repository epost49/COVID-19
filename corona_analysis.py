#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:02:59 2020

@author: Ethan

This script plots COVID-19 time series data.
The data comes from a Johns Hopkins GitHub repo "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data".
The goal is to identify trends in the reported deaths and to quantify the spread.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import helpers as hs

datadir = "/home/ethan/Documents/Code/COVID-19/input_data"
date_dir = "2020-03-28"
#fname = "time_series_19-covid-Deaths.csv"
fname = "time_series_covid19_deaths_global.csv"
fpath = os.path.join(datadir, date_dir, fname)

#states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
states = None  # 3/28 dataset no longer lists states

country_dict = [{'country':'US','states':states,'population':327000000},
                {'country':'Canada','states':None,'population':37600000},
                {'country':'Italy','states':None,'population':60500000}]

df = pd.read_csv(fpath)  # extract DataFrame from csv file

y_max = 1000

i = 1
for c in country_dict:
    data_lists = hs.get_country_total(df, c['country'], c['states'])  # get dictionary of time list and country total list
    x = data_lists['dates']
    y = data_lists['country_total']
    #y_arr = np.array(y)
    #y_arr = np.multiply(np.divide(y_arr,c['population']),1000000)  # deaths per million
    y = np.multiply(np.divide(y,c['population']),1000000)  # deaths per million
    #y = list(y_arr)
    start_index = 20
    x = x[1:]  # remove 1st element so size matches diff array
    y = np.diff(y)  # create array of differences
    hs.plot_figs2(x[start_index:], y[start_index:], c['country'],i,y_max)
    i = i + 1

plt.show()

