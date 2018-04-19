# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:38:30 2018

@author: jblon
"""

import pandas as pd
import numpy as np

pitcher = 'arrij001'

list_balls = ['B','H','I','N','P','V']
list_strikes = ['B','C','F','K','L','M','O','Q','R','S','T','X', 'Y']

fip_constant = {'YEAR_ID' : [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001, 2000], 'cFIP' : [3.107, 3.158, 3.147, 3.134, 3.132, 3.048, 3.095, 3.025, 3.079, 3.097, 3.132, 3.240, 3.147, 3.020, 3.049, 3.031, 2.962, 3.134, 3.049]}

fip_constant = pd.DataFrame(data=fip_constant)


events = pd.read_csv('C:/users/jblon/documents/Pitcher-Rotations/single_game.csv')

events_single=events[events['PIT_ID'] == pitcher]

few_col = events_single[['PIT_ID','INN_CT','YEAR_ID','PA_NEW_FL','PITCH_SEQ_TX', 'EVENT_TX', 'EVENT_CD', 'BATTEDBALL_CD', 'EVENT_RUNS_CT', 'EVENT_OUTS_CT']].copy()

def batted_count(colname, event):
    few_col[colname] = np.where(few_col['BATTEDBALL_CD'] == event, 1, 0)    

def ind_ratio(event):
    col_name = event + '_PER'
    calc = event + '_SUM'
    grouped[col_name] = grouped[calc] / grouped['BIP']
    
def cum_ratio(event):
    col_name = 'CUM_' + event + '_PER'
    calc = 'CUM_' + event + '_SUM'
    grouped[col_name] = grouped[calc] / grouped['CUM_BIP']
    
#Number of hit types
few_col['SINGLE_CT'] = np.where(few_col['EVENT_CD'] == 20, 1, 0) 
few_col['DOUBLE_CT'] = np.where(few_col['EVENT_CD'] == 21, 1, 0)
few_col['TRIPLE_CT'] = np.where(few_col['EVENT_CD'] == 22, 1, 0)
few_col['HR_CT'] = np.where(few_col['EVENT_CD'] == 23, 1, 0)


#Number of hits
few_col['HITS_CT'] = few_col['SINGLE_CT'] + few_col['DOUBLE_CT'] + few_col['TRIPLE_CT'] + few_col['HR_CT']


#Number of walks
temp = few_col[['EVENT_TX']].applymap(lambda x: str.count(x, 'W'))
temp.columns = ['BB_SUM']
few_col = few_col.join(temp)

#Number of HBP
temp = few_col[['EVENT_TX']].applymap(lambda x: str.count(x, 'HP'))
temp.columns = ['HP_SUM']
few_col = few_col.join(temp)

#Number of plate appearances
few_col['PA_CT'] = np.where(few_col['PA_NEW_FL'] == 'T', 1, 0)

#Number of Strikeouts
few_col['SO_CT'] = np.where(few_col['EVENT_CD'] == 3, 1, 0)

#calculate different batted ball counts
batted_count('GB_SUM', 'G') 
batted_count('FB_SUM', 'F')
batted_count('LD_SUM', 'L')
batted_count('PU_SUM', 'P')

#calculate number of balls in play
few_col['BIP'] = np.where((few_col['BATTEDBALL_CD'] == 'G') | 
                          (few_col['BATTEDBALL_CD'] == 'F') | 
                          (few_col['BATTEDBALL_CD'] == 'L') |
                          (few_col['BATTEDBALL_CD'] == 'P') , 1, 0)


#Group bunch of stuff together, and sum, cumulative sum stuff
#Initial grouping, first individual, second cumulative
group_notcum = few_col.groupby(['YEAR_ID', 'PIT_ID','INN_CT']).sum()
group_cum = few_col.groupby(['YEAR_ID', 'PIT_ID', 'INN_CT']).sum().groupby(level=[1]).cumsum()

#Drop some column, add prefix to cumulative columns
group_cum_final = group_cum.drop(['EVENT_CD', 'EVENT_RUNS_CT'], 1)
group_cum_final_rename = group_cum_final.add_prefix('CUM_')

#Merge individual and grouped
grouped = group_notcum.join(group_cum_final_rename)

#Reset index
grouped = grouped.reset_index(level = ['YEAR_ID', 'PIT_ID', 'INN_CT'])

#Calculate ratios
ind_ratio('GB')
ind_ratio('FB')
ind_ratio('LD')
ind_ratio('PU')

#Calculate cumulative ratios
cum_ratio('GB')
cum_ratio('FB')
cum_ratio('LD')
cum_ratio('PU')

#Calculate pitch counts
pitch_counts = few_col.groupby(['YEAR_ID', 'PIT_ID', 'INN_CT'])['PITCH_SEQ_TX'].sum().map(list).apply(pd.value_counts)\
    .fillna(0).astype(int).reset_index()

#Number of balls
pitch_counts['BALLS_CT'] = pitch_counts[pitch_counts.columns.intersection(list_balls)].sum(axis=1)

#Number of strikes
pitch_counts['STRIKES_CT'] = pitch_counts[pitch_counts.columns.intersection(list_strikes)].sum(axis=1)

#Overall number of pitches
pitch_counts['PITCHES'] = pitch_counts['BALLS_CT'] + pitch_counts['STRIKES_CT']

#Number of balls hit into play, should match BIP column
pitch_counts['INPLAY_CT'] = pitch_counts.X

#Number of strikes without hit into play
pitch_counts['STRIKES_CT_WO_PLAY'] = pitch_counts['PITCHES'] - pitch_counts['BALLS_CT'] - pitch_counts['INPLAY_CT']

#Merge other counts with pitch counts
merged = pd.merge(grouped, pitch_counts, on=('PIT_ID', 'YEAR_ID', 'INN_CT'))

#Calculate SO/PA ratio
merged['IND_SO_PA'] = merged['SO_CT'] / merged['PA_CT']
merged['CUM_SO_PA'] = merged['CUM_SO_CT'] / merged['CUM_PA_CT']

#Calculate BB/PA ratio
merged['IND_BB_PA'] = merged['BB_SUM'] / merged['PA_CT']
merged['CUM_BB_PA'] = merged['CUM_BB_SUM'] / merged['CUM_PA_CT']

#Other ratio
merged['IND_GB_PA'] = (merged['GB_SUM'] - merged['FB_SUM'] - merged['PU_SUM']) / merged['PA_CT']
merged['CUM_GB_PA'] = (merged['CUM_GB_SUM'] - merged['CUM_FB_SUM'] - merged['CUM_PU_SUM']) / merged['CUM_PA_CT']

#Other ratio opposite sign + squared
merged['IND_NEG_GB_PA'] = ((merged['GB_SUM'] - merged['FB_SUM'] - merged['PU_SUM']) / merged['PA_CT'])**2

merged['CUM_NEG_GB_PA'] = ((merged['CUM_GB_SUM'] - merged['CUM_FB_SUM'] - merged['CUM_PU_SUM']) / merged['CUM_PA_CT'])**2

merged['IND_NEG_GB_PA'] = np.where(merged['IND_GB_PA'] > 0, -merged['IND_NEG_GB_PA'], merged['IND_NEG_GB_PA'])

merged['CUM_NEG_GB_PA'] = np.where(merged['CUM_GB_PA'] > 0, -merged['CUM_NEG_GB_PA'], merged['CUM_NEG_GB_PA'])

#Calculate individual SIERA
merged['IND_SIERA'] = 6.145 - 16.986*merged['IND_SO_PA'] + 11.434*merged['IND_BB_PA'] - 1.858*merged['IND_GB_PA'] + 7.653*(merged['IND_SO_PA'])**2 + 6.664 *merged['IND_NEG_GB_PA'] + 10.130*merged['IND_SO_PA']*merged['IND_GB_PA'] - 5.195*merged['IND_BB_PA']*merged['IND_GB_PA']


#Calculate cumulative SIERA
merged['CUM_SIERA'] = 6.145 - 16.986*merged['CUM_SO_PA'] + 11.434*merged['CUM_BB_PA'] - 1.858*merged['CUM_GB_PA'] + 7.653*(merged['CUM_SO_PA'])**2 + 6.664 *merged['CUM_NEG_GB_PA'] + 10.130*merged['CUM_SO_PA']*merged['CUM_GB_PA'] - 5.195*merged['CUM_BB_PA']*merged['CUM_GB_PA']

#Merge for FIP constant
merged_FIP = pd.merge(merged, fip_constant, on='YEAR_ID')

#Calculate Innings Pitched
merged['IND_IP'] = merged['EVENT_OUTS_CT'] / 3
merged['CUM_IP'] = merged['CUM_EVENT_OUTS_CT'] / 3

#Calculate FIP
merged['IND_FIP'] = ((13*merged['HR_CT'] + 3*(merged['BB_SUM'] + merged['HP_SUM']) - 2*merged['SO_CT']) / merged['IND_IP']) + merged_FIP['cFIP']

#Calculate cumulative FIP
merged['CUM_FIP'] = ((13*merged['CUM_HR_CT'] + 3*(merged['CUM_BB_SUM'] + merged['CUM_HP_SUM']) - 2*merged['CUM_SO_CT']) / merged['CUM_IP']) + merged_FIP['cFIP']


