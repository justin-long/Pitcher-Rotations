# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:06:44 2018

@author: Justin
"""

import matplotlib.pyplot as plt
import numpy as np

plt.ion()


x = np.arange(0, 35, 1)

plt.plot(pit_mean_std['AT_BATS'], pit_mean_std['SIERA_STD'])
plt.plot(pit_mean_std['AT_BATS'], pit_mean_std['SIERA_MEAN'])

plt.fill_between(x, pit_mean_std['SIERA_STD'], -5, color='lawngreen', alpha='.75')
plt.fill_between(x, 2*pit_mean_std['SIERA_STD'], pit_mean_std['SIERA_STD'], color='yellow', alpha='.75')
plt.fill_between(x, 20*pit_mean_std['SIERA_STD'], 2*pit_mean_std['SIERA_STD'], color='red', alpha='.75')
plt.axhline(y=0, color='black')

plt.ylim(-4,4)
plt.xlim(0, 25)


pit_mean_std2 = pit_mean_std.append([pit_mean_std.tail(1)]*10, ignore_index=True)
pit_mean_std2['AT_BATS'] = pit_mean_std2.index

[pit_mean_std.tail(5)]*2

ax.scatter(self.siera_df.At_Bat,
								  self.siera_df.Siera, c='black')
ax.plot(self.siera_df.At_Bat,
							   self.siera_df.Siera, c='black')

ax.axhline(y=0, color='black')
ax.set_xticks(np.arange(0, 999))
ax.set_ylim([-4, 4])
ax.set_xlim([0,
									self.siera_df.At_Bat.max() +
									1])

draw()


def plot(do_this):
    if do_this == 'init':
        print('hey')
    else:
        print('this')
        
plot('no')

at_bat = 5

temp = pit_mean_std.at[at_bat -1 , 'SIERA_MEAN']

print(temp)


pit_mean_std

temp = pit_mean_std['AT_BATS', 'PIT_ID', 'SIERA_MEAN']