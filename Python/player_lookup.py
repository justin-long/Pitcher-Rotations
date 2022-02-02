# -*- coding: utf-8 -*-
"""
Created on Thu May  3 09:30:54 2018

@author: jblon
"""

import pandas as pd
from datetime import datetime

def player_lookup(name):
    return players_recent.loc[players_recent['full_name'] == name, 'ID'].item()

players = pd.read_csv('C:/Users/jblon/Documents/Datasets/retrosheet_players.txt')

players['start_date'] = pd.to_datetime(players['Player debut'], infer_datetime_format=True)

players['full_name'] = players['First'] + ' ' + players['Last']

players_recent = players[players['start_date'] >= '1980-01-01']

player = 'David Aardsma'
players_recent.loc[players_recent['full_name'] == 'Justin Verlander', 'ID'].item()

player_lookup('Shawn Abner')
