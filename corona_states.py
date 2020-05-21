#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:22:52 2020

@author: ethan
"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import os
import helpers as hs
register_matplotlib_converters()


datadir = os.path.join("input_data","2020-05-20")
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

#state_list = [state_list[2]]

hs.plot_states(df, state_list, 40)
#hs.plot_norm_avg(df, state_list, 7, 40)

plt.show()