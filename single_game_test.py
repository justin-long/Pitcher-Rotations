# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:38:30 2018

@author: jblon
"""

import pandas as pd
import numpy as np

list_balls = ['B','H','I']
list_strikes = ['B','C','F','H','I','L','M','N','O','P','S','T','V', 'X']

events = pd.read_csv('C:/users/jblon/documents/Pitcher-Rotations/single_game.csv')

few_col = events[['PIT_ID','INN_CT','YEAR_ID','PA_NEW_FL','PITCH_SEQ_TX', 'EVENT_TX', 'EVENT_CD', 'BATTEDBALL_CD', 'EVENT_RUNS_CT']].copy()

def batted_count(colname, event):
    few_col[colname] = np.where(few_col['BATTEDBALL_CD'] == event, 1, 0)

#Number of walks
temp = few_col[['EVENT_TX']].applymap(lambda x: str.count(x, 'W'))
temp.columns = ['BB_SUM']
few_col = few_col.join(temp)

#Number of plate appearances
few_col['PA_CT'] = np.where(few_col['PA_NEW_FL'] == 'T', 1, 0)

#Number of Strike Outs
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



group_notcum = few_col.groupby(['YEAR_ID', 'PIT_ID','INN_CT']).sum()
group_cum = few_col.groupby(['YEAR_ID', 'PIT_ID', 'INN_CT']).sum().groupby(level=[1]).cumsum()


group_cum = few_col.groupby(['YEAR_ID', 'PIT_ID', 'INN_CT']).cumsum()
list(group_cum)

group_cum_final = group_cum.drop(['EVENT_CD', 'EVENT_RUNS_CT'], 1)
group_cum_final_rename = group_cum_final.add_prefix('cum_')

final = group_notcum.join(group_cum_final_rename)



group3 = few_col.groupby(['PIT_ID', 'YEAR_ID', ]).sum()

group4 = group3.apply(lambda x: x.cumsum())


#Group and sum, partition by year, pitcher, inning
grouped = few_col.groupby(['YEAR_ID','PIT_ID', 'INN_CT']).sum()

grouped['GB_PER'] = grouped['GB_SUM'] / grouped['BIP']
grouped['FB_PER'] = grouped['FB_SUM'] / grouped['BIP']
grouped['LD_PER'] = grouped['LD_SUM'] / grouped['BIP']
grouped['PU_PER'] = grouped['PU_SUM'] / grouped['BIP']

grouped = grouped.reset_index(level = ['YEAR_ID', 'PIT_ID'])

pitch_counts = few_col.groupby(['PIT_ID', 'YEAR_ID'])['PITCH_SEQ_TX'].sum().map(list).apply(pd.value_counts)\
    .fillna(0).astype(int).reset_index()

#Overall number of pitches
pitch_counts['PITCHES'] = pitch_counts[list_strikes].sum(axis=1) + pitch_counts[list_balls].sum(axis=1)
#Number of balls
pitch_counts['BALLS_CT'] = pitch_counts[list_balls].sum(axis=1)
#Number of strikes
pitch_counts['STRIKES_CT'] = pitch_counts['PITCHES'] - pitch_counts['BALLS_CT']
#Number of balls hit into play
pitch_counts['INPLAY_CT'] = pitch_counts.X
#Number of strikes without hit into play
pitch_counts['STRIKES_CT_WO_PLAY'] = pitch_counts['PITCHES'] - pitch_counts['BALLS_CT'] 
- pitch_counts['INPLAY_CT']

merged = pd.merge(grouped, pitch_counts, on=('PIT_ID', 'YEAR_ID'))

SO_PA = 






grouped['SIERA'] = 6.145 - 16.986*
                
grouped

