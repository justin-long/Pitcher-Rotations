# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:31:33 2018

@author: jblon
"""

import pandas as pd
import numpy as np
import mysql.connector

one_game = pd.read_csv('C:/users/jblon/documents/datasets/one_game_for_char.csv')
one_game
list(one_game)

few_col = one_game[['PIT_ID','PA_NEW_FL','PITCH_SEQ_TX', 'EVENT_TX', 'BATTEDBALL_CD']].copy()

def batted_count(colname, event):
    few_col[colname] = np.where(few_col['BATTEDBALL_CD'] == event, 1, 0)

#Number of walks
temp = few_col[['EVENT_TX']].applymap(lambda x: str.count(x, 'W'))
temp.columns = ['BB_SUM']
few_col = few_col.join(temp)

#Number of plate appearances
few_col['PA_CT'] = np.where(few_col['PA_NEW_FL'] == 'T', 1, 0)

#calculate different batted ball counts
batted_count('GB_SUM', 'G') 
batted_count('FB_SUM', 'F')
batted_count('LD_SUM', 'L')

#calculate number of balls in play
few_col['BIP'] = np.where((few_col['BATTEDBALL_CD'] == 'G') | 
                          (few_col['BATTEDBALL_CD'] == 'F') | 
                          (few_col['BATTEDBALL_CD'] == 'L'), 1, 0)

grouped = few_col.groupby('PIT_ID').sum()

grouped['GB_PER'] = grouped['GB_SUM'] / grouped['BIP']
grouped['FB_PER'] = grouped['FB_SUM'] / grouped['BIP']
grouped['LD_PER'] = grouped['LD_SUM'] / grouped['BIP']


grouped['SIERA'] = 6-17*(grouped['BB_SUM']/grouped['PA_CT'])

grouped



few_col
