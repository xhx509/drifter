# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 11:13:22 2014

@author: hxu

read csv file(data comes from bluefish sensor) and save them to a dataframe, then plot them
"""
import pandas as pd
from dateutil.parser import parse
filename='bluefish2014-11-18 09:36:23.csv'
def bluefish_csv_read(filename):
    df=pd.read_csv(filename,names=['id','time','temp(C)'])
    for k in range(len(df)):
       df.time[k]=parse(df.time[k])
    return df     
df= bluefish_csv_read(filename)      