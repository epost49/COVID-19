#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:22:52 2020

@author: ethan
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
import helpers as hs

datadir = os.path.join("input_data","2020-04-12")
fname = "time_series_covid19_deaths_US.csv"
fpath = os.path.join(os.getcwd(), datadir, fname)

df = pd.read_csv(fpath)  # extract DataFrame from csv file
state_list = [
            {'name':'California', 'pop':39512223},
            {'name':'New York', 'pop':19453561},
            {'name':'Washington', 'pop':7614893},
            {'name':'Louisiana', 'pop':4648794},
            {'name':'New Jersey', 'pop':8882190},
            {'name':'Florida', 'pop':21477737}
            ]
#state_list = ['California', 'New York', 'Washington', 'Louisiana', 'New Jersey', 'Florida']

hs.plot_states(df, state_list, 40)

plt.show()