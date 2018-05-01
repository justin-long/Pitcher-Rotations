# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:13:45 2018

@author: jblon
"""

from PyQt5 import QtWidgets, QtGui
from test_ui import Ui_Siera
import numpy as np
import pandas as pd


class SieraWindow(QtWidgets.QMainWindow, Ui_Siera):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # connect spinboxes
        self.spinBox_BB.valueChanged.connect(self.siera_calc)
        # self.spinBox_Balls.valueChanged.connect(self.siera)
        self.spinBox_FB.valueChanged.connect(self.siera_calc)
        self.spinBox_GB.valueChanged.connect(self.siera_calc)
        # self.spinBox_HR.valueChanged.connect(self.siera)
        # self.spinBox_K.valueChanged.connect(self.siera)
        self.spinBox_PA.valueChanged.connect(self.siera_calc)
        self.spinBox_PU.valueChanged.connect(self.siera_calc)
        self.spinBox_SO.valueChanged.connect(self.siera_calc)

        # connect buttons to table
        self.pushButton_SO.clicked.connect(self.add_table)
        self.pushButton_Walk.clicked.connect(self.add_table)
        self.pushButton_GB.clicked.connect(self.add_table)
        self.pushButton_FB.clicked.connect(self.add_table)
        self.pushButton_PU.clicked.connect(self.add_table)
        self.pushButton_Other.clicked.connect(self.add_table)
        self.pushButton_Delete.clicked.connect(self.remove_row)

    def add_table(self):
        button = self.sender()
        row = self.spinBox_AB_TBL.value()

        rowPosition = self.tableWidget_Events.rowCount()
        self.tableWidget_Events.insertRow(rowPosition)

        self.tableWidget_Events.setItem(rowPosition, 0,
                                        QtWidgets.QTableWidgetItem(str(row)))
        self.tableWidget_Events.setItem(
                rowPosition, 1, QtWidgets.QTableWidgetItem(button.text()))

        self.spinBox_AB_TBL.setValue(self.spinBox_AB_TBL.value() + 1)

        self.dataframe_gen()

    def remove_row(self):
        selected = self.tableWidget_Events.currentRow()
        self.tableWidget_Events.removeRow(selected)

        self.dataframe_gen()

    def dataframe_gen(self):
        num_rows = self.tableWidget_Events.rowCount()
        num_cols = self.tableWidget_Events.columnCount()

        tmp_df = pd.DataFrame(
            columns=['At_Bat_Num', 'Event'], index=range(num_rows))
        for i in range(num_rows):
            for j in range(num_cols):
                tmp_df.ix[i, j] = self.tableWidget_Events.item(i, j).text()
        print(tmp_df)

        self.num_SO = tmp_df.Event.str.count('Strikeout').sum()
        self.num_Walk = tmp_df.Event.str.count('Walk').sum()
        self.num_Other = tmp_df.Event.str.count('Other').sum()
        self.num_GB = tmp_df.Event.str.count('Ground Ball').sum()
        self.num_FB = tmp_df.Event.str.count('Fly Ball').sum()
        self.num_PU = tmp_df.Event.str.count('Pop-Up').sum()
        self.num_PA = (self.num_SO + self.num_Walk + self.num_Other +
                       self.num_GB + self.num_FB + self.num_PU)

        self.label_SO_ct.setText(str(self.num_SO))
        self.label_Walk_ct.setText(str(self.num_Walk))
        self.label_Other_ct.setText(str(self.num_Other))
        self.label_GB_ct.setText(str(self.num_GB))
        self.label_FB_ct.setText(str(self.num_FB))
        self.label_PU_ct.setText(str(self.num_PU))
        self.label_PA_ct.setText(str(self.num_PA))

    def siera_calc(self):
        SO_PA = self.spinBox_SO.value() / self.spinBox_PA.value()
        BB_PA = self.spinBox_BB.value() / self.spinBox_PA.value()
        GB_PA = (self.spinBox_GB.value() -
                 self.spinBox_FB.value() -
                 self.spinBox_PU.value()) / self.spinBox_PA.value()
        GB_PA_SQ = GB_PA ** 2
        GB_PA_SQ_OPP = np.where(GB_PA > 0, -GB_PA_SQ, GB_PA_SQ)

        mean = self.mean
        stdev = self.stdev

        SIERA = (
                6.145 - 16.986 * SO_PA + 11.434 * BB_PA - 1.858 * GB_PA +
                7.653 * (SO_PA ** 2) + 6.664 * GB_PA_SQ_OPP +
                10.130 * (SO_PA * GB_PA) - 5.195 * (BB_PA * GB_PA)
                )
        SIERA_str = str(SIERA)

        SIERA_Standard = (SIERA - mean) / stdev
        SIERA_Standard_str = str(SIERA_Standard)

        self.label_SIERA.setText(SIERA_str)
        self.label_SIERA_STD.setText(SIERA_Standard_str)

    def siera_comp(pitcher, metric):
        list_balls = [
                'B', 'H', 'I', 'N', 'P', 'V'
                ]
        list_strikes = [
                'C', 'F', 'K', 'L', 'M', 'O',
                'Q', 'R', 'S', 'T', 'X', 'Y'
                ]

        fip_constant = {
                'YEAR_ID': [
                        2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011,
                        2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003,
                        2002, 2001, 2000
                        ],
                'cFIP': [
                        3.107, 3.158, 3.147, 3.134, 3.132, 3.048, 3.095,
                        3.025, 3.079, 3.097, 3.132, 3.240, 3.147, 3.020,
                        3.049, 3.031, 2.962, 3.134, 3.049
                        ]}

        fip_constant = pd.DataFrame(data=fip_constant)

        events = pd.read_csv(
                'C:/users/jblon/documents/Pitcher-Rotations/cle_2015_2016.csv'
                )

        events_single = events[events['PIT_ID'] == pitcher]

        few_col = events_single[[
                'PIT_ID', 'INN_CT', 'YEAR_ID', 'PA_NEW_FL', 'PITCH_SEQ_TX',
                'EVENT_TX',  'EVENT_CD',  'BATTEDBALL_CD',  'EVENT_RUNS_CT',
                'EVENT_OUTS_CT', 'GAME_ID'
                ]].copy()

        def batted_count(colname, event):
            few_col[colname] = np.where(
                    few_col['BATTEDBALL_CD'] == event, 1, 0)

        def ind_ratio(event):
            col_name = event + '_PER'
            calc = event + '_SUM'
            grouped[col_name] = grouped[calc] / grouped['BIP']

        def cum_ratio(event):
            col_name = 'CUM_' + event + '_PER'
            calc = 'CUM_' + event + '_SUM'
            grouped[col_name] = grouped[calc] / grouped['CUM_BIP']

        def SIERA(x, ind):
            return(
                    6.145 - 16.986 * x[ind + '_SO_PA'] +
                    11.434 * x[ind + '_BB_PA'] -
                    1.858 * x[ind + '_GB_PA'] +
                    7.653*(x[ind + '_SO_PA'])**2 +
                    6.664 * x[ind + '_NEG_GB_PA'] +
                    10.130 * x[ind + '_SO_PA'] * x[ind + '_GB_PA'] -
                    5.195 * x[ind + '_BB_PA'] * x[ind + '_GB_PA']
                    )

        # Number of hit types
        few_col['SINGLE_CT'] = np.where(few_col['EVENT_CD'] == 20, 1, 0)
        few_col['DOUBLE_CT'] = np.where(few_col['EVENT_CD'] == 21, 1, 0)
        few_col['TRIPLE_CT'] = np.where(few_col['EVENT_CD'] == 22, 1, 0)
        few_col['HR_CT'] = np.where(few_col['EVENT_CD'] == 23, 1, 0)

        # Number of hits
        few_col['HITS_CT'] = (
                few_col['SINGLE_CT'] + few_col['DOUBLE_CT'] +
                few_col['TRIPLE_CT'] + few_col['HR_CT']
                )

        # Number of walks
        temp = few_col[['EVENT_TX']].applymap(lambda x: str.count(x, 'W'))
        temp.columns = ['BB_SUM']
        few_col = few_col.join(temp)

        # Number of HBP
        temp = few_col[['EVENT_TX']].applymap(lambda x: str.count(x, 'HP'))
        temp.columns = ['HP_SUM']
        few_col = few_col.join(temp)

        # Number of plate appearances
        few_col['PA_CT'] = np.where(few_col['PA_NEW_FL'] == 'T', 1, 0)

        # Number of Strikeouts
        few_col['SO_CT'] = np.where(few_col['EVENT_CD'] == 3, 1, 0)

        # calculate different batted ball counts
        batted_count('GB_SUM', 'G')
        batted_count('FB_SUM', 'F')
        batted_count('LD_SUM', 'L')
        batted_count('PU_SUM', 'P')

        # calculate number of balls in play
        few_col['BIP'] = np.where((few_col['BATTEDBALL_CD'] == 'G') |
                                  (few_col['BATTEDBALL_CD'] == 'F') |
                                  (few_col['BATTEDBALL_CD'] == 'L') |
                                  (few_col['BATTEDBALL_CD'] == 'P'), 1, 0)

        # Group bunch of stuff together
        # Initial grouping, first individual
        grouped = few_col.groupby(['GAME_ID', 'PIT_ID']).sum()

        # Reset index
        grouped = grouped.reset_index(level=['GAME_ID', 'PIT_ID'])

        # Calculate ratios
        ind_ratio('GB')
        ind_ratio('FB')
        ind_ratio('LD')
        ind_ratio('PU')

        # Calculate pitch counts
        pitch_counts = (
                few_col.groupby(['GAME_ID', 'PIT_ID'])
                ['PITCH_SEQ_TX'].sum().map(list).apply(pd.value_counts)
                .fillna(0).astype(int).reset_index()
                )

        # Number of balls
        pitch_counts['BALLS_CT'] = (
                pitch_counts[(pitch_counts.columns.
                              intersection(list_balls))].sum(axis=1)
                )

        # Number of strikes
        pitch_counts['STRIKES_CT'] = (
                pitch_counts[pitch_counts.columns.intersection(list_strikes)]
                .sum(axis=1)
                )

        # Overall number of pitches
        pitch_counts['PITCHES'] = (
                pitch_counts['BALLS_CT'] + pitch_counts['STRIKES_CT']
                )

        # Number of balls hit into play, should match BIP column
        pitch_counts['INPLAY_CT'] = pitch_counts.X

        # Number of strikes without hit into play
        pitch_counts['STRIKES_CT_WO_PLAY'] = (
                pitch_counts['PITCHES'] -
                pitch_counts['BALLS_CT'] -
                pitch_counts['INPLAY_CT']
                )

        # Merge other counts with pitch counts
        merged = pd.merge(grouped, pitch_counts, on=('GAME_ID', 'PIT_ID'))

        # Calculate SO/PA ratio
        merged['IND_SO_PA'] = merged['SO_CT'] / merged['PA_CT']

        # Calculate BB/PA ratio
        merged['IND_BB_PA'] = merged['BB_SUM'] / merged['PA_CT']

        # Other ratio
        merged['IND_GB_PA'] = (
                (merged['GB_SUM'] - merged['FB_SUM'] - merged['PU_SUM']) /
                merged['PA_CT']
                )

        # Other ratio opposite sign + squared
        merged['IND_NEG_GB_PA'] = (
                ((merged['GB_SUM'] - merged['FB_SUM'] - merged['PU_SUM']) /
                 merged['PA_CT'])**2
                 )

        merged['IND_NEG_GB_PA'] = np.where(
                merged['IND_GB_PA'] > 0,
                -merged['IND_NEG_GB_PA'],
                merged['IND_NEG_GB_PA']
                )

        # Calculate individual SIERA
        merged['IND_SIERA'] = SIERA(merged, 'IND')

        # Fix year_id
        merged['YEAR_ID'] = pd.to_numeric(merged.GAME_ID.str[3:7])

        # Merge for FIP constant
        merged_FIP = pd.merge(merged, fip_constant, on='YEAR_ID')

        # Calculate Innings Pitched
        merged['IND_IP'] = merged['EVENT_OUTS_CT'] / 3

        # Calculate FIP
        merged['IND_FIP'] = (
                ((13*merged['HR_CT'] + 3*(merged['BB_SUM'] +
                  merged['HP_SUM']) - 2*merged['SO_CT']) / (merged['IND_IP']) +
                  merged_FIP['cFIP'])
                )

        # Drop some columns
        final_stats = merged.drop('EVENT_CD', 1)

        # Calculate Mean, St.Dev
        pit_mean = final_stats['IND_SIERA'].mean()
        pit_stdev = final_stats['IND_SIERA'].std()

        if metric == 'mean':
            return pit_mean
        if metric == 'stdev':
            return pit_stdev

    mean = siera_comp('klubc001', 'mean')
    stdev = siera_comp('klubc001', 'stdev')
