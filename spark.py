#!/usr/bin/env python
# coding: utf-8

import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import pandas as pd
import os
import shutil
from os import walk

spark = SparkSession.builder.appName("Python Spark SQL basic example").getOrCreate()

col_spec = [(0, 6), (7, 12), (13, 41), (42, 46), (47, 50), (51, 55), (56, 63), (64, 73), (73, 80), (81, 89), (90, 97)]

'''
data_dict = {}
data_dict['lat'] = []
data_dict['lon'] = []

for dirpath, dirnames, filenames in os.walk('data2019/'):
#     print(os.path.join("/", "USA_station_data"))
    for filename in filenames:
        usaf_id_this_file = filename[:6]
        wban_id_this_file = filename[7:12]

        if usaf_id_this_file in usaf_id_list and wban_id_this_file in wban_id_list:
            print(usaf_id_this_file)
            print('done')
            temp = data_usa[data_usa['USAF'] == usaf_id_this_file]
            lat = temp['LAT']
            lon = temp['LON']
            
            data_dict['lat'].append(lat)
            data_dict['lon'].append(lon)
            
            
            print(lat, lon)
            source = os.path.join(dirpath, filename)
            print(source)
            dest = "./USA_station_data"
            shutil.copy(source, dest)
'''



col_spec2 = [(0, 6), (7, 13), (14, 25), (26, 36), (37,-1)]

for dirpath, dirnames, filenames in os.walk("USA_station_data/"):
    for filename in filenames:
        data_df = pd.read_fwf(os.path.join(dirpath, filename))
        print(data_df.shape)


id_coordinates = pd.read_csv('id_world_coord.csv')

usaf_id_list = set(id_coordinates['USAF'])
wban_id_list = set(id_coordinates['WBAN'])

col_spec2 = [(0, 6), (7, 13), (14, 25), (26, 36), (37, -1)]

dataframe_created = False
index = 1
for dirpath, dirnames, filenames in os.walk('data2019/'):
    for filename in filenames:
        usaf_id_this_file = int(filename[:6])
        wban_id_this_file = int(filename[7:12])
        # print(usaf_id_this_file, wban_id_this_file)

        temp = id_coordinates[id_coordinates['USAF'] == usaf_id_this_file]

        temp = temp[temp['WBAN'] == wban_id_this_file]
        
        file = os.path.join(dirpath, filename)
        temperature_data = pd.read_fwf(file)
        temperature_data = temperature_data.filter(['YEARMODA', 'TEMP'])
        if temperature_data.empty or temp.empty:
            continue
        if not dataframe_created:
            cols = ['LAT', 'LON'] + list(temperature_data['YEARMODA'])
            print(cols)
            df = pd.DataFrame(columns=cols)
            dataframe_created = True
            
        data_dict = {}
        
        data_dict['LAT'] = temp.iloc[0]['LAT']
        data_dict['LON'] = temp.iloc[0]['LON']
        data_dict.update(dict(zip(temperature_data.YEARMODA, temperature_data.TEMP)))
#         print(data_dict)
        
        df.loc[index] = pd.Series(data_dict)
        index += 1
        
df.to_csv("myRes.csv")


def getStations(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, data=df):
    result_df = data[data['LAT'] <= topLeftLat]
    result_df = result_df[result_df['LAT'] >= bottomRightLat]
    result_df = result_df[result_df['LON'] <= topLeftLong]
    result_df = result_df[result_df['LON'] >= bottomRightLong]
    return result_df

subset_test = getStations(80.06, 16.06, 59.03, 5.34)
print(subset_test)
