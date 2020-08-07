#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 17:26:58 2020

@author: ethan
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def c19_pmpw(row, age_dict):
    # COVID-19 deaths per million per week
    weeks = (row['End Week'] - row['Start week']).days/7
    out = 1000000*row['COVID-19 Deaths']/age_dict[row['Age group']]/weeks
    return out

def tot_deaths_pmpw(row, age_dict):
    # Total deaths per million per week
    weeks = (row['End Week'] - row['Start week']).days/7
    out = 1000000*row['Total Deaths']/age_dict[row['Age group']]/weeks
    return out

def round_down(x):
    # Rounds down to nearest power of 10
    return 10**(np.floor(np.log10(x)))

def round_up(x):
    # Rounds up to nearest multiple of n, where n is nearest rounded down
    # power of 10
    return np.ceil(x/round_down(x))*round_down(x)

def hbar_plot(cats, vals, vlabel, title, fname):
    y_pos = np.arange(len(cats))
    
    plt.barh(y_pos, vals, align='center', color='#a2aaff')
    plt.yticks(y_pos, cats)
    plt.xlabel(vlabel)
    plt.xlim(round_down(np.min(vals)), round_up(np.max(vals)))
    plt.xscale('log')
    plt.title(title)
    plt.tight_layout()
    
    plt.savefig(fname, format='pdf')
    plt.clf()


# Import CDC COVID-19 dataset
df = pd.read_csv('CDC_data/Provisional_COVID-19_Death_Counts_by_Sex__Age__and_State.csv', 
                parse_dates=['Start week', 'End Week'])

# Age distribution data from https://www.census.gov/data/tables/2019/demo/age-and-sex/2019-age-sex-composition.html
# Build a dictionary of age groups to populations
keys = ['0-4 years', '5-14 years', '15-24 years', '25-34 years',
       '35-44 years', '45-54 years', '55-64 years', '65-74 years',
       '75-84 years','85 years and over']
vals = [19736000, 41039000, 42103000, 45209000, 41027000, 40700000, 41755000, 
        31487000, 15407000, 5893000]
age_dist = dict()
for k, v in zip(keys, vals):
    age_dist[k] = v
age_dist

# Filter for US data and combined male/female data
filt = (df['State'] == 'United States') & (df['Sex'] == 'All')
usdf = df.loc[filt]

# Combine 'Under 1 year' and '1-4 years' age groups into '0-4 years' so that U.S. population data can be incorporated
r1yr = usdf.loc[usdf['Age group'] == 'Under 1 year']
r1to4yrs = usdf.loc[usdf['Age group'] == '1-4 years']
r0to4yrs = r1yr.copy()
r0to4yrs['Age group'] = '0-4 years'
pd.options.mode.chained_assignment = None  # default='warn'
cols = ['COVID-19 Deaths', 'Total Deaths', 'Pneumonia Deaths', 'Pneumonia and COVID-19 Deaths', 'Influenza Deaths', 'Pneumonia, Influenza, or COVID-19 Deaths']
for c in cols:
    r0to4yrs[c] = r1yr[c].to_numpy() + r1to4yrs[c].to_numpy()
    
# Prepend a row for 0-4 years
usdf2 = pd.concat([r0to4yrs, usdf]).reset_index(drop = True)

# Remove the 'All Ages' and redundant age categories
indexNames = usdf2[(usdf2['Age group'] == 'All Ages') | (usdf2['Age group'] == 'Under 1 year') | (usdf2['Age group'] == '1-4 years')].index
usdf3 = usdf2.drop(indexNames)

# Create new columns with normalized data
usdf3['COVID-19 Deaths per Million per Week'] = usdf3.apply(lambda x: c19_pmpw(x, age_dist), axis=1)
usdf3['Total Deaths per Million per Week'] = usdf3.apply(lambda x: tot_deaths_pmpw(x, age_dist), axis=1)
usdf3['Non-COVID-19 Deaths per Million per Week'] = usdf3.apply(lambda x: tot_deaths_pmpw(x, age_dist) - c19_pmpw(x, age_dist), axis=1)
usdf3['Percent of total deaths due to COVID-19'] = usdf3.apply(lambda x: 100*x['COVID-19 Deaths']/x['Total Deaths'], axis=1)
usdf3['Non-COVID-19 to COVID-19 Death Ratio'] = usdf3.apply(lambda x: (x['Total Deaths']-x['COVID-19 Deaths'])/x['COVID-19 Deaths'], axis=1)

# Make bar charts of data and save them to file
cats = usdf3['Age group'].to_numpy()
cols = ['COVID-19 Deaths per Million per Week',
        'Total Deaths per Million per Week',
        'Non-COVID-19 Deaths per Million per Week',
        'Percent of total deaths due to COVID-19',
        'Non-COVID-19 to COVID-19 Death Ratio']

for col in cols:
    hbar_plot(cats, usdf3[col].to_numpy(), '', col, col)
    