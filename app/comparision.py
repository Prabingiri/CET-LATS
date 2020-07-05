# methods = request.form.getlist('check')
# dataset = request.form.get('data')
# print(methods, dataset)
# Compress Ratio for PAA and DFT
import csv
from app.compress_methods import compress
from app.distance_metrics_final import distance_metrics
import os
import json
from app import app

from flask import jsonify, make_response

import pandas as pd
methods = ['PAA', 'VW']
dataset= 'cluster1'
ratios = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
result = dict()

# Error tolerance for DP, VW and OPT
errors = [15, 25, 35, 50, 65, 80]
if os.path.exists('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt'):
    # data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')
    print("compression started......")
    dm = distance_metrics(dataset)
    rawvolume = dm.raw_volfor1cluster()
    # b=dm.raw_volfor1cluster()
    print("raw volume calculated")
    method = set(methods)
    headers = ['d_metric', 'c_method', '1/c_ratio', 'measure', 'value']
    d = open('comparison_result.csv', 'w')
    w = csv.writer(d)
    w.writerow(headers)
    d.close()
    # d.write(headers)
    if 'VW' in method:
        data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')

        compress_data = {}
        for datapoint in data:
            # print("I am inside for loop")
            datapoint = datapoint.split(',')
            lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

            if (lon, lat) not in compress_data:
                # print('Start dealing with ', str(lon), str(lat))
                time_series = [float(each_one) for each_one in datapoint[2:]]
                compress_data[(lon, lat)] = dict()
                # compression_m_body = compression_method_body(time_series)
                c_tools = compress(time_series)
                for error in errors:
                    compress_data[(lon, lat)][('VW', error)] = c_tools.modify_vw(error)

        hd = dm.Hausdarff_distance(rawvolume, compress_data)
        ad = dm.Angular_diff(rawvolume, compress_data)

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in hd.items():
            for key_measure, vals in mm.items():
                write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))

                # d.writerow(headers)
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in ad.items():
            for key_measure, vals in mm.items():
                write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for error in errors:

            compressedvolume = dm.compressed_volume(rawvolume, error, 'VW', compress_data)
                # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
            vol_diff = dm.volume_difference(rawvolume, compressedvolume)

            for each_tec, mm in vol_diff.items():
                for key_measure, vals in mm.items():
                    write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
        d.close()

        print("I am done with vw")


    if 'PAA' in method:
        compress_data = {}
        data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')

        for datapoint in data:
            datapoint = datapoint.split(',')
            lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

            if (lon, lat) not in compress_data:
                # print('Start dealing with ', str(lon), str(lat))
                time_series = [float(each_one) for each_one in datapoint[2:]]
                compress_data[(lon, lat)] = dict()
                c_tools = compress(time_series)
                for ratio in ratios:
                    compress_data[(lon, lat)][('PAA', ratio)] = c_tools.paa(ratio)

        hd = dm.Hausdarff_distance(rawvolume, compress_data)
        ad = dm.Angular_diff(rawvolume, compress_data)

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in hd.items():
            for key_measure, vals in mm.items():
                write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in ad.items():
            for key_measure, vals in mm.items():
                write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for ratio in ratios:

            compressedvolume = dm.compressed_volume(rawvolume, ratio, 'PAA', compress_data)

            vol_diff = dm.volume_difference(rawvolume, compressedvolume)

            for each_tec, mm in vol_diff.items():
                for key_measure, vals in mm.items():
                    write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals)/len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
        d.close()


        print("I am done with PAA")
    if 'DFT' in method:
        compress_data = {}
        data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')

        for datapoint in data:
            datapoint = datapoint.split(',')
            lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

            if (lon, lat) not in compress_data:
                # print('Start dealing with ', str(lon), str(lat))
                time_series = [float(each_one) for each_one in datapoint[2:]]
                compress_data[(lon, lat)] = dict()
                c_tools = compress(time_series)
                for ratio in ratios:
                    compress_data[(lon, lat)][('DFT', ratio)] = c_tools.dft(ratio)

        hd = dm.Hausdarff_distance(rawvolume, compress_data)
        ad = dm.Angular_diff(rawvolume, compress_data)

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in hd.items():
            for key_measure, vals in mm.items():
                write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in ad.items():
            for key_measure, vals in mm.items():
                write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for ratio in ratios:

            compressedvolume = dm.compressed_volume(rawvolume, ratio, 'DFT', compress_data)

            vol_diff = dm.volume_difference(rawvolume, compressedvolume)

            for each_tec, mm in vol_diff.items():
                for key_measure, vals in mm.items():
                    write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals)/len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
        d.close()

        print("I am done with DFT")

    if 'OP' in method:
        data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')

        compress_data = {}
        for datapoint in data:
            # print("I am inside for loop")
            datapoint = datapoint.split(',')
            lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

            if (lon, lat) not in compress_data:
                # print('Start dealing with ', str(lon), str(lat))
                time_series = [float(each_one) for each_one in datapoint[2:]]
                compress_data[(lon, lat)] = dict()
                # compression_m_body = compression_method_body(time_series)
                c_tools = compress(time_series)
                for error in errors:
                    compress_data[(lon, lat)][('OP', error)] = c_tools.modify_opt(error)

        hd = dm.Hausdarff_distance(rawvolume, compress_data)
        ad = dm.Angular_diff(rawvolume, compress_data)

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in hd.items():
            for key_measure, vals in mm.items():
                write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))

                # d.writerow(headers)
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in ad.items():
            for key_measure, vals in mm.items():
                write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        for error in errors:

            compressedvolume = dm.compressed_volume(rawvolume, error, 'OP', compress_data)
                # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
            vol_diff = dm.volume_difference(rawvolume, compressedvolume)

            for each_tec, mm in vol_diff.items():
                for key_measure, vals in mm.items():
                    write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
        d.close()

        print("I am done with OP")


    if 'DP' in method:
        data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')

        compress_data = {}
        for datapoint in data:
            # print("I am inside for loop")
            datapoint = datapoint.split(',')
            lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

            if (lon, lat) not in compress_data:
                # print('Start dealing with ', str(lon), str(lat))
                time_series = [float(each_one) for each_one in datapoint[2:]]
                compress_data[(lon, lat)] = dict()
                # compression_m_body = compression_method_body(time_series)
                c_tools = compress(time_series)
                for error in errors:
                    compress_data[(lon, lat)][('DP', error)] = c_tools.modify_dp(error)

        hd = dm.Hausdarff_distance(rawvolume, compress_data)
        ad = dm.Angular_diff(rawvolume, compress_data)

        d = open('comparison_result.csv', 'a')
        for each_tec, mm in hd.items():
            for key_measure, vals in mm.items():
                write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))

                # d.writerow(headers)
                d.write('\n')
        d.close()

        d = open('comparison_result.csv', 'a')
        write_list=[]
        for each_tec, mm in ad.items():
            for key_measure, vals in mm.items():
                write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                d.write(",".join([str(x) for x in write_list]))
                d.write('\n')
        d.close()


        d = open('comparison_result.csv', 'a')
        for error in errors:

            compressedvolume = dm.compressed_volume(rawvolume, error, 'DP', compress_data)
                # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
            vol_diff = dm.volume_difference(rawvolume, compressedvolume)

            for each_tec, mm in vol_diff.items():
                for key_measure, vals in mm.items():
                    write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
        d.close()

        print("I am done with DP")



    # with open('comparison_result.csv', 'r') as csvdata:
    #     next(csvdata, None)  # skip the headers
    #     reader = csv.DictReader(csvdata, fieldnames=['d_metric', 'c_method', '1/c_ratio', 'measure', 'value'])
    #     json.dump([row for row in reader], open('output.json', 'w+'))
    # reader = csv.DictReader('comparison_result.csv','r')

    # response = app.response_class(
    #     response=json.dumps([row for row in reader]),
    #     status=200,
    #     mimetype='application/json'
    # )
    # print(response.data)
    import pandas as pd

    # csv_dict = dict()
    # with open('comparison_result.csv', 'r') as csvdata:
    #     for row, column in csvdata:
    #         csv_dict[row] = column
    #
    # dump_variable = json.dumps(csv_dict)
    # print(dump_variable)

    with open('comparison_result.csv', 'r') as csvdata:
        next(csvdata, None)  # skip the headers
        reader = csv.DictReader(csvdata, fieldnames=['d_metric', 'c_method', '1/c_ratio', 'measure', 'value'])
        json.dump([row for row in reader], open('comparison.json', 'w+'))


else:

    print( "data is not available")
