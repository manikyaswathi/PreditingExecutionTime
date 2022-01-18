#!/usr/bin/env python

import glob
import pandas as pd
import re, os
from datetime import datetime

#file_path = '06_tau/parallels/sg-1'
'''
file_paths = ['001_tau_ds1', '001_tau_ds2', '001_tau_ds3', '01_tau', '02_tau', '03_tau', '04_tau', '05_tau', '06_tau_old', '07_tau_s1', '07_tau_s2', '07_tau_s3', '07_tau_s4', '07_tau_s5', '07_tau_s6', '07_tau_s7', '07_tau_s8', '08_tau_s1', '08_tau_s2', '08_tau_s3', '08_tau_s4', '08_tau_s5', '08_tau_s6']
'''

file_paths = ['campaign_4L_Mix']

file_pattern = 'codar.post.details.*'

frames_L = []

for file_path in file_paths:
	# print("Path =" + str(file_path + "/" + file_pattern))
	list_files = glob.glob(file_path +"/parallels/sg-1/" + file_pattern)
	# print("*****"+str(list_files))
	
	frames = []
	for file in list_files:
	    data = pd.read_csv(file)  
	    frames.append(data)
	    
	print("**********************"+ file_path)
	if len(frames) > 0: print(len(frames))
	else: print("NO DATA")
	frames_L = frames_L + frames

if len(frames_L) > 0:
	df = pd.concat(frames_L)
	print("Training Data", len(frames_L))
	df.to_csv('training_data_4L_SE_MIX2.csv', header=True, index=False)
else: 
	print("NO DATA AT ALL")
