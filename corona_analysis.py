#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:02:59 2020

@author: Ethan

This script plots COVID-19 time series data.
The data comes from a Johns Hopkins GitHub repo "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data".
The goal is to identify trends in the reported deaths and to quantify the spread.
"""

import matplotlib.pyplot as plt
import pandas as pd
import sys
import helpers as hs
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

fpath = sys.argv[1]

#states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
states = None  # 3/28 dataset no longer lists states

country_dict = [{'country':'US','states':states,'population':327000000},
                {'country':'Canada','states':None,'population':37600000},
                {'country':'Italy','states':None,'population':60461826},
                {'country':'France','states':None,'population':65273511},
                {'country':'Germany','states':None,'population':83783942},
                {'country':'United Kingdom','states':None,'population':67886011},
                {'country':'Spain','states':states,'population':46940000},
                {'country':'Belgium','states':states,'population':11460000},
                {'country':'Sweden','states':states,'population':10230000}]

country_dict = [country_dict[i] for i in (0,1,2)]
#country_dict = [country_dict[i] for i in (2,3,4,5)]

df = pd.read_csv(fpath)  # extract DataFrame from csv file

y_max = 1000

#hs.plot_figs4(df, country_dict, y_max)
#hs.plot_figs5(df, country_dict, y_max)
hs.plot_figs5(df, country_dict, y_max)

plt.show()

