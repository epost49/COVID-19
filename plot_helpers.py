#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:18:04 2020

@author: ethan
"""
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import datetime as dt

def get_country_total(df, country_label, states=None):
    # This function takes in a pandas DataFrame and a "Country/Region" label to
    # produce a list of dates and a list of country totals, packaged in a 
    # dictionary. The DataFrame comes from a csv file in a particular format.
    
    #date_list = df.columns.values.tolist()[4:]  # convert DataFrame header to a list, and remove first 4 elements
    date_list = df.columns.values[4:]  # convert DataFrame header to an array, and remove first 4 elements
    vfunc = np.vectorize(lambda x : dt.datetime.strptime(x,"%m/%d/%y").date())  # create vector function for date format conversion
    #formatted_dates = [dt.datetime.strptime(d,"%m/%d/%y").date() for d in date_list]
    formatted_dates = vfunc(date_list)
    country_rows = df.loc[df['Country/Region'] == country_label]  # extract rows for desired country
    if states:
        country_rows = country_rows.loc[country_rows['Province/State'].isin(states)]  # extract rows with state names
        
    country_rows2 = country_rows.drop(['Province/State','Country/Region','Lat','Long'],axis=1)  # remove unwanted columns
    country_row_tot = country_rows2.apply(np.sum,axis=0)  # sum all the country values
    #country_tot_list = country_row_tot.values.tolist()  # convert DataFrame to a list
    country_tot_list = country_row_tot.values  # convert DataFrame to an array
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
    axarr[1].set_ylim(.01, y_max)
    axarr[1].grid(True, axis='y')
    
    for tick in axarr[1].get_xticklabels():
        tick.set_rotation(55)
    
    plt.tight_layout()
    plt.figure(fign)