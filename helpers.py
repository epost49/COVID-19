#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:18:04 2020

@author: ethan
"""
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

def get_country_total(df, country_label, states=None):
    # This function takes in a pandas DataFrame and a "Country/Region" label to
    # produce a list of dates and a list of country totals, packaged in a 
    # dictionary. The DataFrame comes from a csv file in a particular format.
    
    date_list = df.columns.values[4:]  # convert DataFrame header to an array, and remove first 4 elements
    vfunc = np.vectorize(lambda x : dt.datetime.strptime(x,"%m/%d/%y").date())  # create vector function for date format conversion
    formatted_dates = vfunc(date_list)
    country_rows = df.loc[df['Country/Region'] == country_label]  # extract rows for desired country
    if states:
        country_rows = country_rows.loc[country_rows['Province/State'].isin(states)]  # extract rows with state names
        
    country_rows2 = country_rows.drop(['Province/State','Country/Region','Lat','Long'],axis=1)  # remove unwanted columns
    country_row_tot = country_rows2.apply(np.sum,axis=0)  # sum all the country values
    country_tot_arr = country_row_tot.values  # convert DataFrame to an array
    out = {'dates':formatted_dates, 'country_total':country_tot_arr}
    
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
    
def moving_average(arr, n):
    out = np.array([])
    for i in range(n, len(arr) + 1):
        out = np.append(out, np.average(arr[(i - n):i]))

    return out

def plot_figs3(x,y,country_label,fign,y_max):
    
    f, axarr = plt.subplots(3,1, sharex=True)

    axarr[0].plot(x, y)
    axarr[0].set_title('COVID-19 deaths per million (' + country_label + ')')
    axarr[0].grid(True, axis='y')
    axarr[1].semilogy(x, y)
    axarr[1].set_ylim(.01, y_max)
    axarr[1].grid(True, axis='y')
    
    # calculate daily changes
    x = x[1:]  # remove 1st element so size matches diff array
    y = np.diff(y)  # create array of differences
    
    # plot moving averages of daily changes
    labels = []
    for n in [3, 7, 14]:
        axarr[2].plot(x[n-1:], moving_average(y, n))
        labels.append(str(n) + " day avg")

    axarr[2].grid(True, axis='y')
    axarr[2].legend(labels)
    axarr[2].set(ylabel='Daily Change')
    
    # make X-axis dates more legible
    for tick in axarr[2].get_xticklabels():
        tick.set_rotation(55)
    
    plt.tight_layout()
    plt.figure(num=fign)
    fig = plt.gcf()
    fig.set_size_inches(4.5, 6.2)

def plot_fig4(df, country_dict, y_max, start_index=20):
    i = 1
    for c in country_dict:
        data_arrays = get_country_total(df, c['country'], c['states'])  # get dictionary of time list and country total list
        x = data_arrays['dates']
        y = data_arrays['country_total']
        y = np.multiply(np.divide(y,c['population']),1000000)  # deaths per million
        plot_figs3(x[start_index:], y[start_index:], c['country'],i,y_max)
        i = i + 1
   
def plot_fig5(df, country_dict, y_max, start_index=20):
    f, axarr = plt.subplots(3, len(country_dict), sharex=True)
    
    i = 0
    for c in country_dict:
        data_arrays = get_country_total(df, c['country'], c['states'])  # get dictionary of time list and country total list
        x = data_arrays['dates']
        y = data_arrays['country_total']
        y = np.multiply(np.divide(y,c['population']),1000000)  # deaths per million
        
        axarr[0, i].plot(x, y)
        #axarr[0, i].set_title('COVID-19 deaths per million (' + c['country'] + ')')
        axarr[0, i].set_title(c['country'])
        axarr[0, i].grid(True, axis='y')
        axarr[1, i].semilogy(x, y)
        axarr[1, i].set_ylim(.01, y_max)
        axarr[1, i].grid(True, axis='y')
        
        # calculate daily changes
        x = x[1:]  # remove 1st element so size matches diff array
        y = np.diff(y)  # create array of differences
        
        # plot moving averages of daily changes
        labels = []
        for n in [3, 7, 14]:
            axarr[2, i].plot(x[n-1:], moving_average(y, n))
            labels.append(str(n) + " day avg")
    
        axarr[2, i].grid(True, axis='y')
        axarr[2, i].legend(labels)
        #axarr[2, i].set(ylabel='Daily Change')
        
        # make X-axis dates more legible
        for tick in axarr[2, i].get_xticklabels():
            tick.set_rotation(55)
            
        i = i + 1
    
    axarr[0, 0].set(ylabel='Cumulative')
    axarr[1, 0].set(ylabel='Cumulative (log scale)')
    axarr[2, 0].set(ylabel='Daily Change')
    f.suptitle('COVID-19 deaths per million')
    plt.gcf().subplots_adjust(bottom=0.15)
    #plt.gcf().text(0, 0, "hello", fontsize=10)
    #plt.tight_layout()
     
     