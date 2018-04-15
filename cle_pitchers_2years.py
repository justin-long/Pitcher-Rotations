# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:31:33 2018

@author: jblon
"""

import pandas as pd
import numpy as np

events = pd.read_csv('C:/users/jblon/documents/Pitcher-Rotations/cle_2015_2016.csv')
events
list(events)

few_col = events[['PIT_ID','YEAR_ID','PA_NEW_FL','PITCH_SEQ_TX', 'EVENT_TX', 'EVENT_CD', 'BATTEDBALL_CD', 'PA_NEW_FL']].copy()

few_col.head()

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
                          (few_col['BATTEDBALL_CD'] == 'L'), 1, 0)

grouped = few_col.groupby(['YEAR_ID','PIT_ID']).sum()

grouped['GB_PER'] = grouped['GB_SUM'] / grouped['BIP']
grouped['FB_PER'] = grouped['FB_SUM'] / grouped['BIP']
grouped['LD_PER'] = grouped['LD_SUM'] / grouped['BIP']
grouped['PU_PER'] = grouped['PU_SUM'] / grouped['BIP']

grouped.head()


grouped = grouped.reset_index(level = ['YEAR_ID', 'PIT_ID'])

grouped['SIERA'] = 6.145 - 16.986*
                
grouped

