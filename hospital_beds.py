#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:52:00 2020

@author: ethan

data source:  https://www.cdc.gov/nhsn/covid19/report-patient-impact.html
download link:  https://www.cdc.gov/nhsn/pdfs/covid19/covid19-NatEst.csv
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# This script makes plots showing the percent occupancy of inpatient and ICU
# hospital beds over time during the COVID-19 pandemic. These plots can provide
# insight into the severity of the pandemic and the appropriateness of loosening
# or tightening constraints on the economy.

def moving_average(arr, n):
    out = np.array([])
    for i in range(0, len(arr)):
        out = np.append(out, np.average(arr[max((i - n + 1),0):i + 1]))

    return out

# Import data and ignore 2nd header row
d_parser = lambda x: pd.datetime.strptime(x,'%d%b%Y')
df = pd.read_csv('covid19-NatEst.csv', skiprows=[1], parse_dates=['collectionDate'], date_parser=d_parser)
df.set_index('collectionDate')

# List of locations to filter
locations = ['US', 'CA','FL']

for l in locations:
    # Filter data by location
    filt = df['state'] == l
    fdf = df.loc[filt]
    
    # Append columns for 7-day moving averages of data
    pd.options.mode.chained_assignment = None  # default='warn'
    newcol1 = 'InBedsOccAnyPat__Numbeds_Est (7-day moving avg)'
    newcol2 = 'InBedsOccCOVID__Numbeds_Est (7-day moving avg)'
    newcol3 = 'ICUBedsOccAnyPat__N_ICUBeds_Est (7-day moving avg)'
    fdf[newcol1] = moving_average(fdf['InBedsOccAnyPat__Numbeds_Est'].to_numpy(), 7)
    fdf[newcol2] = moving_average(fdf['InBedsOccCOVID__Numbeds_Est'].to_numpy(), 7)
    fdf[newcol3] = moving_average(fdf['ICUBedsOccAnyPat__N_ICUBeds_Est'].to_numpy(), 7)
    
    # Create plot and set formatting
    statename = str(fdf.loc[fdf['state']==l]['statename'].iloc[0])
    
    ax = fdf.plot(x='collectionDate',ylim=(0,100),
          y=[newcol1,
             newcol2,
             newcol3],
             title=statename+" hospital bed occupancy during COVID-19")
    ax.get_xaxis().get_label().set_visible(False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=55)
    ax.set_ylabel("Percent occupancy")
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()
    
    # Save figure
    plt.savefig(os.path.join("hospital_figs", statename + ".pdf"))
