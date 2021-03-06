from app import app
from flask import request, render_template, redirect
from flask import jsonify, make_response
# from app.distance_metrics import distance_metrics
from app.compress_methods import compress
from app.distance_metrics_final import distance_metrics
from app.prediction import predict_methods
from csv import DictReader
from itertools import groupby
from pprint import pprint
from app.visualization import visualize
import os
import csv
import json
from statistics import mean
import os
from flask import flash, url_for
from werkzeug.utils import secure_filename
import numpy as np

UPLOAD_FOLDER = 'app/static/dataset/rawa_data'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import pandas as pd






temperature_dataset = pd.read_csv("app/static/dataset/rawa_data/myRes.csv", index_col=0)
@app.route('/')
def index():
    datasets = os.listdir(UPLOAD_FOLDER)
    li = [x.split('.')[0] for x in datasets]
    print(li)
    methods = {
        'Discrete Fourier Transform (DFT)': [0.1, 0.15, 0.2, 0.25, 0.3, 0.5],
        'Piecewise Aggregate Approximation (PAA)': [0.1, 0.15, 0.2, 0.25, 0.3, 0.5],
        'Visvalingam-Whyatt Algorithm (VW)' : [15, 25, 35, 50, 65, 80],
        '(Adapted) Optimal Algorithm (OP)': [15, 25, 35, 50, 65, 80],
        '(Adapted) Douglas-Peucker Algorithm (DP)': [15, 25, 35, 50, 65, 80]
    }

    return render_template("public/index.html", methods=methods, datasets=li)




@app.route("/individual_results", methods=["POST", "GET"])

def input_comparision():
    # request.form.get
    c_method = request.form.get("method")
    compression_ratio = request.form.get("ratio")
    dataset = request.form.get("data")
    # lat1 = 59
    # lat2 =70
    # lon1 = 6
    # lon2 = -9
    # dataset2 = pd.read_csv("app/static/dataset/rawa_data/myRes.csv", index_col=0)

    # function_1(lat1,lat2, lon1,lon2):
    #     dataset = "cluster1"
    #     return dataset
    #

    print(dataset)
    print(c_method)
    print(compression_ratio)

    # def getStations(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, data):
    #     result_df = data[data['LAT'] >= topLeftLat]
    #     result_df = result_df[result_df['LAT'] <= bottomRightLat]
    #     result_df = result_df[result_df['LON'] <= topLeftLong]
    #     result_df = result_df[result_df['LON'] >= bottomRightLong]
    #     return result_df
    #
    # subset_data = getStations(lat1, lon1, lat2, lon2, dataset2)
    # if len(subset_data) == 0:
    #     print("Data is not available!")
    #
    # print(subset_data)
    # subset_data_dict_show = subset_data.set_index('LAT')['LON'].to_dict()
    # print(subset_data_dict_show)

    def fix(user_input):
        mapping = {"Discrete Fourier Transform (DFT)": "DFT", "Piecewise Aggregate Approximation (PAA)": "PAA",
                   "Visvalingam-Whyatt Algorithm (VW)": "VW", "(Adapted) Optimal Algorithm (OP)": "OP",
                    "(Adapted) Douglas-Peucker Algorithm (DP)": "DP"
                   }

        return mapping.get(user_input, user_input)
    compression_method = fix(c_method)
    print(compression_method)

    # if request.is_json:
    #
    #     req = request.get_json()
    #     dataset = req.get("dataset")
    # dataset ='6'
    #     # print(dataset)
    #
    #     compression_method = req.get("compression_method")
    #     compression_ratio = req.get("compression_ratio")
    #     # method = req.get("method")
    #     raw_volume ={}
    compress_data = dict()
    if compression_method and compression_ratio is not None:

        #
        # if len(subset_data)!=0:
        if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')
            # data = subset_data
            print("compression started......")
            dm = distance_metrics(dataset)
            rawvolume = dm.raw_volfor1cluster()
            print("raw volume calculated")
            headers = ['d_metric', 'c_method', 'c_ratio', 'measure', 'value']
            d = open('app/static/results/individual_result.csv', 'w')
            w = csv.writer(d)
            w.writerow(headers)
            d.close()

            # c_m_body = compression_method_body()
            if compression_method == "DFT":

                    print("I am inside DFT")
                # self.compress_data[(lon, lat)] = dict()
                    for datapoint in data:
                        # print("I am inside for loop")
                        datapoint = datapoint.split(',')
                        lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
                        if ((lon, lat) and (compression_method and compression_ratio)) not in compress_data:
                            # print("I am inside if lat lon condition")
                            print('Start dealing with ', str(lon), str(lat))
                            time_series = [float(each_one) for each_one in datapoint[2:]]
                            compress_data[(lon, lat)] = dict()
                            c_tools = compress(time_series)

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.dft(float(compression_ratio))

                    print("I was already compressed ")
                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method,
                                                            compress_data)

                    print("compressed volume is calculated")

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in hd.items():
                        for key_measure, vals in mm.items():
                            write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))

                            # d.writerow(headers)
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in ad.items():
                        for key_measure, vals in mm.items():
                            write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()



                    with open('app/static/results/individual_result.csv') as csvfile:
                        r = DictReader(csvfile, skipinitialspace=True)
                        data = [dict(d) for d in r]

                        groups = []
                        uniquekeys = []

                        for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['c_ratio'])):
                            groups.append({
                                "d_metric": k[0],
                                "c_method": k[1],
                                "c_ratio": k[2],
                                "values": [
                                    {k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'c_ratio']} for d
                                    in list(g)]
                            })
                            uniquekeys.append(k)
                    print(groups)

                    # result = json.dumps((groups), open('app/static/results/comparison.json', 'w+')))
                    # res = make_response(result, 200)
                    with open('app/static/results/individual_results.json', 'w') as f:
                        json.dump(groups, f)
                    return render_template("public/bargraph.html", method=compression_method, compression_ratio=compression_ratio)
                    # with open('app/static/results/individual_result.csv') as csvfile:
                    #     r = DictReader(csvfile, skipinitialspace=True)
                    #     data = [dict(d) for d in r]
                    #
                    #     groups = []
                    #     uniquekeys = []
                    #
                    #     for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['c_ratio'])):
                    #         groups.append({
                    #             "d_metric": k[0],
                    #             "c_method": k[1],
                    #             "c_ratio": k[2],
                    #             "values": [
                    #                 {k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'c_ratio']} for d
                    #                 in list(g)]
                    #         })
                    #         uniquekeys.append(k)
                    # result = jsonify(groups)
                    # res = make_response(result, 200)
                    # with open("app/static/dataset/data.json", "r") as read_file:
                    #     print("Converting JSON encoded data into Python dictionary")
                    #     developer = json.load(read_file)
                    # return jsonify(developer)


                    # pprint(groups)

                    # with open('app/static/results/individual_result.csv') as csvrdr:
                    #     reader = csv.reader(csvrdr)
                    #     data_list = list()
                    #     for row in reader:
                    #         data_list.append(row)
                    # jdata = [dict(zip(data_list[0], row)) for row in data_list]
                    # jdata.pop(0)
                    # result = jsonify(jdata)
                    # res = make_response(result, 200)
                    # print(res)
                    # return res

            elif compression_method == "PAA":

                    print("I am inside PAA")
                # self.compress_data[(lon, lat)] = dict()
                    for datapoint in data:
                        # print("I am inside for loop")
                        datapoint = datapoint.split(',')
                        lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
                        if (lon, lat) not in compress_data:
                            # print("I am inside if lat lon condition")
                            print('Start dealing with ', str(lon), str(lat))
                            time_series = [float(each_one) for each_one in datapoint[2:]]
                            compress_data[(lon, lat)] = dict()

                            c_tools = compress(time_series)

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.paa(float(compression_ratio))
                        else:

                            print("I was already compressed ")
                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method,
                                                            compress_data)

                    print("compressed volume is calculated")

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in hd.items():
                        for key_measure, vals in mm.items():
                            write_list = ['Hausdorff Distance', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))

                            # d.writerow(headers)
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in ad.items():
                        for key_measure, vals in mm.items():
                            write_list = ['Angular Difference', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['Volumetric Difference', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()

                    with open('app/static/results/individual_result.csv') as csvfile:
                        r = DictReader(csvfile, skipinitialspace=True)
                        data = [dict(d) for d in r]

                        groups = []
                        uniquekeys = []

                        for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['c_ratio'])):
                            groups.append({
                                "d_metric": k[0],
                                "c_method": k[1],
                                "c_ratio": k[2],
                                "values": [
                                    {k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'c_ratio']} for d
                                    in list(g)]
                            })
                            uniquekeys.append(k)
                    print(groups)

                    # result = json.dumps((groups), open('app/static/results/comparison.json', 'w+')))
                    # res = make_response(result, 200)
                    with open('app/static/results/individual_results.json', 'w') as f:
                        json.dump(groups, f)
                    return render_template("public/bargraph.html", method=compression_method, compression_ratio=compression_ratio)

                    # a= json.dumps(groups)


                        # f.write()
                    # res = make_response(result, 200)

                    # with open('app/static/results/comparison_result.csv', 'r') as csvdata:
                    #     next(csvdata, None)  # skip the headers
                    #     reader = csv.DictReader(csvdata, fieldnames=['d_metric', 'c_method', 'c_ratio', 'measure', 'value'])
                    #     json.dump([row for row in reader], open('app/static/results/comparison.json', 'w+'))

                    # return render_template("/public/Comparison.html", methods=method, json_result_url
                    # return res
                    # with open("app/static/dataset/data.json", "r") as read_file:
                    #     print("Converting JSON encoded data into Python dictionary")
                    #     developer = json.load(read_file)
                    # return jsonify(developer)
                    # with open('app/static/results/individual_result.csv') as csvrdr:
                    #     reader = csv.reader(csvrdr)
                    #     data_list = list()
                    #     for row in reader:
                    #         data_list.append(row)
                    # jdata = [dict(zip(data_list[0], row)) for row in data_list]
                    # jdata.pop(0)
                    # result = jsonify(jdata)
                    # res = make_response(result, 200)
                    # print(res)
                    # return res

            elif compression_method == "DP":

                    print("I am inside DP")
                # self.compress_data[(lon, lat)] = dict()
                    for datapoint in data:
                        # print("I am inside for loop")
                        datapoint = datapoint.split(',')
                        lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
                        if (lon, lat) not in compress_data:
                            # print("I am inside if lat lon condition")
                            print('Start dealing with ', str(lon), str(lat))
                            time_series = [float(each_one) for each_one in datapoint[2:]]
                            compress_data[(lon, lat)] = dict()

                            c_tools = compress(time_series)

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.modify_dp(int(compression_ratio))

                    print("I was already compressed ")
                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method,
                                                            compress_data)

                    print("compressed volume is calculated")

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in hd.items():
                        for key_measure, vals in mm.items():
                            write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))

                            # d.writerow(headers)
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in ad.items():
                        for key_measure, vals in mm.items():
                            write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()
                    with open('app/static/results/individual_result.csv') as csvfile:
                        r = DictReader(csvfile, skipinitialspace=True)
                        data = [dict(d) for d in r]

                        groups = []
                        uniquekeys = []

                        for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['c_ratio'])):
                            groups.append({
                                "d_metric": k[0],
                                "c_method": k[1],
                                "c_ratio": k[2],
                                "values": [
                                    {k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'c_ratio']} for d
                                    in list(g)]
                            })
                            uniquekeys.append(k)
                    print(groups)

                    # result = json.dumps((groups), open('app/static/results/comparison.json', 'w+')))
                    # res = make_response(result, 200)
                    with open('app/static/results/individual_results.json', 'w') as f:
                        json.dump(groups, f)
                    return render_template("public/bargraph.html", method=compression_method, compression_ratio=compression_ratio)


            elif compression_method == "VW":

                    print("I am inside VW")
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

                            compress_data[(lon, lat)][(compression_method, compression_ratio)] = c_tools.modify_vw(int(compression_ratio))

                        else:

                            print("I was already compressed ")
                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method,
                                                            compress_data)

                    print("compressed volume is calculated")

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in hd.items():
                        for key_measure, vals in mm.items():
                            write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))

                            # d.writerow(headers)
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in ad.items():
                        for key_measure, vals in mm.items():
                            write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()
                    with open('app/static/results/individual_result.csv') as csvfile:
                        r = DictReader(csvfile, skipinitialspace=True)
                        data = [dict(d) for d in r]

                        groups = []
                        uniquekeys = []

                        for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['c_ratio'])):
                            groups.append({
                                "d_metric": k[0],
                                "c_method": k[1],
                                "c_ratio": k[2],
                                "values": [
                                    {k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'c_ratio']} for d
                                    in list(g)]
                            })
                            uniquekeys.append(k)
                    print(groups)

                    # result = json.dumps((groups), open('app/static/results/comparison.json', 'w+')))
                    # res = make_response(result, 200)
                    with open('app/static/results/individual_results.json', 'w') as f:
                        json.dump(groups, f)
                    return render_template("public/bargraph.html", method=compression_method, compression_ratio=compression_ratio)

            elif compression_method == "OP":

                    print("I am inside OP")
                # self.compress_data[(lon, lat)] = dict()
                    for datapoint in data:
                        # print("I am inside for loop")
                        datapoint = datapoint.split(',')
                        lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
                        if ((lon, lat) and (compression_method and compression_ratio)) not in compress_data:
                            # print("I am inside if lat lon condition")
                            print('Start dealing with ', str(lon), str(lat))
                            time_series = [float(each_one) for each_one in datapoint[2:]]
                            compress_data[(lon, lat)] = dict()

                            c_tools = compress(time_series)

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.modify_opt(int(compression_ratio))

                    print("I was already compressed ")
                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method,
                                                            compress_data)

                    print("compressed volume is calculated")

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in hd.items():
                        for key_measure, vals in mm.items():
                            write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))

                            # d.writerow(headers)
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')
                    for each_tec, mm in ad.items():
                        for key_measure, vals in mm.items():
                            write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()

                    d = open('app/static/results/individual_result.csv', 'a')

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                    d.close()



                    with open('app/static/results/individual_result.csv') as csvfile:
                        r = DictReader(csvfile, skipinitialspace=True)
                        data = [dict(d) for d in r]

                        groups = []
                        uniquekeys = []

                        for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['c_ratio'])):
                            groups.append({
                                "d_metric": k[0],
                                "c_method": k[1],
                                "c_ratio": k[2],
                                "values": [
                                    {k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'c_ratio']} for d
                                    in list(g)]
                            })
                            uniquekeys.append(k)
                    print(groups)

                    # result = json.dumps((groups), open('app/static/results/comparison.json', 'w+')))
                    # res = make_response(result, 200)
                    with open('app/static/results/individual_results.json', 'w') as f:
                        json.dump(groups, f)
                    return render_template("public/bargraph.html", method=compression_method, compression_ratio=compression_ratio)
                    # with open('app/static/results/individual_result.csv') as csvrdr:
                    #     reader = csv.reader(csvrdr)
                    #     data_list = list()
                    #     for row in reader:
                    #         data_list.append(row)
                    # jdata = [dict(zip(data_list[0], row)) for row in data_list]
                    # jdata.pop(0)
                    # result = jsonify(jdata)
                    # res = make_response(result, 200)
                    # print(res)
                    # return res


        else:
              return make_response(jsonify({"message": " Dataset is not available"}), 400)

    else:
        # print(compress_data)

        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@app.route("/visualize")
def TIN_visualize():
    datasets = os.listdir(UPLOAD_FOLDER)
    li = [x.split('.')[0] for x in datasets]
    return render_template("public/visualization.html", datasets=li)

@app.route("/visualize_results", methods=["POST"])
def visualization():
    from app.visualization import visualize
    compression_method = request.form.get("compression")
    instance = request.form.get("s_instance")
    dataset = request.form.get("data")
    print(compression_method)
    print(instance)
    # data = open('app/static/dataset/rawa_data/cluster1.txt', 'r')

    # dataset = 'cluster6'
    v = visualize(dataset)
    # v.__init__('6')
    # # visual.plotting()
    # val_idx = instance
    ratio = 0.5
    lon, lat, z = v.val_and_lon_lat(val_idx=int(instance)+2)
    # print(z)
    if compression_method =='DFT':

        cm_points = v.compresse_interpolate(dataset=dataset, mthd=v.dft, datatype=float, ratio=ratio)
        z2 = v.interpolated_zvalue(val_idx=0, interpolated_points=cm_points)
        # print(z2)
        v.plotting(lon=lon, lat=lat, z_raw=z, z_compress=z2, mthd=compression_method, ratio=ratio)
        return render_template("/public/visualize_TINinstance.html", method=compression_method, instance=instance, file_name='/images/TINinstance/3D{0}.png'.format(compression_method.lower()))

    elif compression_method == 'PAA':

        cm_points = v.compresse_interpolate(dataset=dataset, mthd=v.paa, datatype=float, ratio=ratio)
        z2 = v.interpolated_zvalue(val_idx=0, interpolated_points=cm_points)
        v.plotting(lon=lon, lat=lat, z_raw=z, z_compress=z2, mthd=compression_method, ratio=ratio)
        return render_template("/public/visualize_TINinstance.html", method=compression_method, instance=instance, file_name='/images/TINinstance/3D{0}.png'.format(compression_method.lower()))

    elif compression_method == 'VW':

        cm_points = v.compresse_interpolate(dataset=dataset, mthd=v.modify_vw, datatype=int, ratio=ratio)
        z2 = v.interpolated_zvalue(val_idx=0, interpolated_points=cm_points)
        v.plotting(lon=lon, lat=lat, z_raw=z, z_compress=z2, mthd=compression_method, ratio=ratio)
        return render_template("/public/visualize_TINinstance.html", method=compression_method, instance=instance, file_name='/images/TINinstance/3D{0}.png'.format(compression_method.lower()))

    elif compression_method == 'DP':

        cm_points = v.compresse_interpolate(dataset=dataset, mthd=v.modify_dp, datatype=int, ratio=ratio)
        z2 = v.interpolated_zvalue(val_idx=0, interpolated_points=cm_points)
        v.plotting(lon=lon, lat=lat, z_raw=z, z_compress=z2, mthd=compression_method, ratio=ratio)
        return render_template("/public/visualize_TINinstance.html", method=compression_method, instance=instance, file_name='/images/TINinstance/3D{0}.png'.format(compression_method.lower()))

    elif compression_method == 'OP':

        cm_points = v.compresse_interpolate(dataset=dataset, mthd=v.modify_opt, datatype=int, ratio=ratio)
        z2 = v.interpolated_zvalue(val_idx=0, interpolated_points=cm_points)
        v.plotting(lon=lon, lat=lat, z_raw=z, z_compress=z2, mthd=compression_method, ratio=ratio)
        return render_template("/public/visualize_TINinstance.html", method=compression_method, instance=instance, file_name='/images/TINinstance/3D{0}.png'.format(compression_method.lower()))

    else:

        return "No compression method is selected"




@app.route("/compare_compression")
def compare_methods():
    datasets = os.listdir(UPLOAD_FOLDER)
    li = [x.split('.')[0] for x in datasets]
    return render_template("public/compare_methods.html", datasets=li)



    # if request.is_json:
    #
    #     req = request.get_json()
    #     dataset = req.get("dataset")
    #     print(dataset)
    #
    #     # compression_method = req.get("compression_method")
    #     # compression_ratio = req.get("compression_ratio")
    #     # method = req.get("method")
    #     raw_volume ={}
    #     methods = req.POST.get("methods")
    #
    #     #
    #
    #     if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
    #         data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')
    #         print("compression started......")
    #         dm = distance_metrics(dataset)
    #         rawvolume = dm.raw_volfor1cluster()
    #         print("raw volume calculated")
    #
    #
    #         for mthod in methods:
    #             if mthod == "DFT":
    #               print("I might work")


@app.route('/comparison', methods=['POST'])
def comparison():
    # user_name = request.form.get('user_input')
    # min_time = request.form.get('min_time')
    # max_time = request.form.get('max_time')
    # compress_data=dict()
    methods = request.form.getlist('check')
    d_method = request.form.getlist('d_method')
    print(methods)
    dataset = request.form.get('data')
    print(methods, dataset, d_method)
    print(d_method)
    # Compress Ratio for PAA and DFT

    rat_ios = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]

    # Error tolerance for DP, VW and OPT
    err_ors = [15, 25, 35, 50, 65, 80]
    compression_level = 2
    ratios = rat_ios
    errors = err_ors
    print(ratios)
    print(errors)
    d_method = np.array(d_method)

    if os.path.exists('app/static/dataset/rawa_data/'+dataset+'.txt'):
        # data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')
        print("compression started......")
        dm = distance_metrics(dataset)
        rawvolume = dm.raw_volfor1cluster()
        # b=dm.raw_volfor1cluster()
        print("raw volume calculated")
        method = set(methods)
        headers = ['d_metric', 'c_method', 'measure', 'value']
        d = open('app/static/results/comparison_result.csv', 'w')
        w = csv.writer(d)
        w.writerow(headers)
        d.close()
        f = open('app/static/results/comparison_mean_result.csv', 'w')
        wr = csv.writer(f)
        wr.writerow(headers)
        f.close()
        # headers2 = ['d_metric', 'c_method', 'measure', 'value']
        # d.write(headers)
        if 'VW' in method:
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')

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


            if d_method=='HD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for each_tec, mm in hd.items():
                    for key_measure, vals in mm.items():
                        write_list = ['HD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))

                        # d.writerow(headers)
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()

                # with open('app/static/results/comparison_result.csv') as csvfile:
                #     r = DictReader(csvfile, skipinitialspace=True)
                #     datam = [dict(d) for d in r]
                #     # datam.pop(0)
                #     # print(datam)
                #
                #     data = {}
                #     for item in datam:
                #         # print(item)
                #         data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                #     # print(data)
                #     f = open('app/static/results/comparison_mean_result.csv', 'a')
                #     for k, v in data.items():
                #         # print(data.items())
                #         ave = mean(float(n) if n else 0 for n in v)
                #         write_list = [*k, ave]
                #         f.write(",".join([str(x) for x in write_list]))
                #         f.write('\n')
                #     f.close()
            elif d_method =='AD':
                d = open('app/static/results/comparison_result.csv', 'a')
                write_list = []
                for each_tec, mm in ad.items():
                    for key_measure, vals in mm.items():
                        write_list = ['AD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            elif d_method =='VD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for error in errors:

                    compressedvolume = dm.compressed_volume(rawvolume, error, 'VW', compress_data)
                    # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                d.close()

                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            else:
                print("No distance metric is selected")



            # d = open('app/static/results/comparison_result.csv', 'a')
            # for each_tec, mm in ad.items():
            #     for key_measure, vals in mm.items():
            #         write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #         d.write(",".join([str(x) for x in write_list]))
            #         d.write('\n')
            # d.close()
            #
            # d = open('app/static/results/comparison_result.csv', 'a')
            # for error in errors:
            #
            #     compressedvolume = dm.compressed_volume(rawvolume, error, 'VW', compress_data)
            #     # print(type(compressedvolume))
            #
            #     # vol_dif.append(vol_diff)
            #     vol_diff = dm.volume_difference(rawvolume, compressedvolume)
            #
            #     for each_tec, mm in vol_diff.items():
            #         for key_measure, vals in mm.items():
            #             write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #             d.write(",".join([str(x) for x in write_list]))
            #             d.write('\n')
            # d.close()

            print("I am done with vw")

        if 'PAA' in method:
            compress_data = {}
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')

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


            if d_method=='HD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for each_tec, mm in hd.items():
                    for key_measure, vals in mm.items():
                        write_list = ['HD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))

                        # d.writerow(headers)
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()

                # with open('app/static/results/comparison_result.csv') as csvfile:
                #     r = DictReader(csvfile, skipinitialspace=True)
                #     datam = [dict(d) for d in r]
                #     # datam.pop(0)
                #     # print(datam)
                #
                #     data = {}
                #     for item in datam:
                #         # print(item)
                #         data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                #     # print(data)
                #     f = open('app/static/results/comparison_mean_result.csv', 'a')
                #     for k, v in data.items():
                #         # print(data.items())
                #         ave = mean(float(n) if n else 0 for n in v)
                #         write_list = [*k, ave]
                #         f.write(",".join([str(x) for x in write_list]))
                #         f.write('\n')
                #     f.close()
            elif d_method =='AD':
                d = open('app/static/results/comparison_result.csv', 'a')
                write_list = []
                for each_tec, mm in ad.items():
                    for key_measure, vals in mm.items():
                        write_list = ['AD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            elif d_method =='VD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for ratio in ratios:

                    compressedvolume = dm.compressed_volume(rawvolume, ratio, 'PAA', compress_data)
                    # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                d.close()

                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            else:
                print("No distance metric is selected")
            #     data = [dict(d) for d in r]
            #
            #     groups = []
            #     uniquekeys = []
            #
            #     for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['measure'])):
            #         groups.append({
            #             "d_metric": k[0],
            #             "c_method": k[1],
            #             "measure": k[2],
            #             "values": [
            #                 {k: v.mean() for k, v in d.items() if k not in ['d_metric', 'c_method', 'measure']} for d
            #                 in list(g)]
            #         })
            #         uniquekeys.append(k)
            # print(groups)

            #
            # with open('app/static/results/individual_result.csv') as csvfile:
            #     r = DictReader(csvfile, skipinitialspace=True)
            #     array = [dict(d) for d in r]
            #
            #     for item in array:
            #         data.append((item[0], item[1]), []).append(item[2])
            #         for k, v in d.items():
            #             print(sum(v) / len(v))

            #     groups = []
            #     uniquekeys = []
            #
            #     for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'], r['measure'])):
            #         groups.append({
            #             "d_metric": k[0],
            #             "c_method": k[1],
            #             "c_measure": k[2],
            #             "values": [{
            #                 k: v for k, v in d.items() if k not in ['d_metric', 'c_method', 'measure']} for d
            #                 in list(g)]
            #         })
            #         uniquekeys.append()
            # print(groups)

            # d = open('app/static/results/comparison_result.csv', 'a')
            # for each_tec, mm in ad.items():
            #     for key_measure, vals in mm.items():
            #         write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #         d.write(",".join([str(x) for x in write_list]))
            #         d.write('\n')
            # d.close()
            #
            # d = open('app/static/results/comparison_result.csv', 'a')
            # for ratio in ratios:
            #
            #     compressedvolume = dm.compressed_volume(rawvolume, ratio, 'PAA', compress_data)
            #
            #     vol_diff = dm.volume_difference(rawvolume, compressedvolume)
            #
            #     for each_tec, mm in vol_diff.items():
            #         for key_measure, vals in mm.items():
            #             write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #             d.write(",".join([str(x) for x in write_list]))
            #             d.write('\n')
            # d.close()

            print("I am done with PAA")
        if 'DFT' in method:
            compress_data = {}
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')

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


            if d_method=='HD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for each_tec, mm in hd.items():
                    for key_measure, vals in mm.items():
                        write_list = ['HD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))

                        # d.writerow(headers)
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()

                # with open('app/static/results/comparison_result.csv') as csvfile:
                #     r = DictReader(csvfile, skipinitialspace=True)
                #     datam = [dict(d) for d in r]
                #     # datam.pop(0)
                #     # print(datam)
                #
                #     data = {}
                #     for item in datam:
                #         # print(item)
                #         data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                #     # print(data)
                #     f = open('app/static/results/comparison_mean_result.csv', 'a')
                #     for k, v in data.items():
                #         # print(data.items())
                #         ave = mean(float(n) if n else 0 for n in v)
                #         write_list = [*k, ave]
                #         f.write(",".join([str(x) for x in write_list]))
                #         f.write('\n')
                #     f.close()
            elif d_method =='AD':
                d = open('app/static/results/comparison_result.csv', 'a')
                write_list = []
                for each_tec, mm in ad.items():
                    for key_measure, vals in mm.items():
                        write_list = ['AD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            elif d_method =='VD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for ratio in ratios:

                    compressedvolume = dm.compressed_volume(rawvolume, ratio, 'DFT', compress_data)
                    # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                d.close()

                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            else:
                print("No distance metric is selected")

            # d = open('app/static/results/comparison_result.csv', 'a')
            # for each_tec, mm in ad.items():
            #     for key_measure, vals in mm.items():
            #         write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #         d.write(",".join([str(x) for x in write_list]))
            #         d.write('\n')
            # d.close()
            #
            # d = open('app/static/results/comparison_result.csv', 'a')
            # for ratio in ratios:
            #
            #     compressedvolume = dm.compressed_volume(rawvolume, ratio, 'DFT', compress_data)
            #
            #     vol_diff = dm.volume_difference(rawvolume, compressedvolume)
            #
            #     for each_tec, mm in vol_diff.items():
            #         for key_measure, vals in mm.items():
            #             write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #             d.write(",".join([str(x) for x in write_list]))
            #             d.write('\n')
            # d.close()

            print("I am done with DFT")

        if 'OP' in method:
            data = open('app/static/dataset/rawa_data/'+dataset+'.txt', 'r')

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


            if d_method=='HD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for each_tec, mm in hd.items():
                    for key_measure, vals in mm.items():
                        write_list = ['HD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))

                        # d.writerow(headers)
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()

                # with open('app/static/results/comparison_result.csv') as csvfile:
                #     r = DictReader(csvfile, skipinitialspace=True)
                #     datam = [dict(d) for d in r]
                #     # datam.pop(0)
                #     # print(datam)
                #
                #     data = {}
                #     for item in datam:
                #         # print(item)
                #         data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                #     # print(data)
                #     f = open('app/static/results/comparison_mean_result.csv', 'a')
                #     for k, v in data.items():
                #         # print(data.items())
                #         ave = mean(float(n) if n else 0 for n in v)
                #         write_list = [*k, ave]
                #         f.write(",".join([str(x) for x in write_list]))
                #         f.write('\n')
                #     f.close()
            elif d_method =='AD':
                d = open('app/static/results/comparison_result.csv', 'a')
                write_list = []
                for each_tec, mm in ad.items():
                    for key_measure, vals in mm.items():
                        write_list = ['AD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            elif d_method =='VD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for error in errors:

                    compressedvolume = dm.compressed_volume(rawvolume, error, 'OP', compress_data)
                    # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                d.close()

                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            else:
                print("No distance metric is selected")

            # d = open('app/static/results/comparison_result.csv', 'a')
            # for each_tec, mm in ad.items():
            #     for key_measure, vals in mm.items():
            #         write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #         d.write(",".join([str(x) for x in write_list]))
            #         d.write('\n')
            # d.close()
            #
            # d = open('app/static/results/comparison_result.csv', 'a')
            # for error in errors:
            #
            #     compressedvolume = dm.compressed_volume(rawvolume, error, 'OP', compress_data)
            #     # print(type(compressedvolume))
            #
            #     # vol_dif.append(vol_diff)
            #     vol_diff = dm.volume_difference(rawvolume, compressedvolume)
            #
            #     for each_tec, mm in vol_diff.items():
            #         for key_measure, vals in mm.items():
            #             write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
            #             d.write(",".join([str(x) for x in write_list]))
            #             d.write('\n')
            # d.close()

            print("I am done with OP")

        if 'DP' in method:
            data = open('app/static/dataset/rawa_data/'+dataset+'.txt', 'r')

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
            print(d_method)
            # d_method = np.array(d_method)
            if d_method=='HD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for each_tec, mm in hd.items():
                    for key_measure, vals in mm.items():
                        write_list = ['HD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))

                        # d.writerow(headers)
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()

                # with open('app/static/results/comparison_result.csv') as csvfile:
                #     r = DictReader(csvfile, skipinitialspace=True)
                #     datam = [dict(d) for d in r]
                #     # datam.pop(0)
                #     # print(datam)
                #
                #     data = {}
                #     for item in datam:
                #         # print(item)
                #         data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                #     # print(data)
                #     f = open('app/static/results/comparison_mean_result.csv', 'a')
                #     for k, v in data.items():
                #         # print(data.items())
                #         ave = mean(float(n) if n else 0 for n in v)
                #         write_list = [*k, ave]
                #         f.write(",".join([str(x) for x in write_list]))
                #         f.write('\n')
                #     f.close()
            elif d_method =='AD':
                d = open('app/static/results/comparison_result.csv', 'a')
                write_list = []
                for each_tec, mm in ad.items():
                    for key_measure, vals in mm.items():
                        write_list = ['AD', each_tec[0], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
                d.close()
                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            elif d_method =='VD':
                d = open('app/static/results/comparison_result.csv', 'a')
                for error in errors:

                    compressedvolume = dm.compressed_volume(rawvolume, error, 'DP', compress_data)
                    # print(type(compressedvolume))

                    # vol_dif.append(vol_diff)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                    for each_tec, mm in vol_diff.items():
                        for key_measure, vals in mm.items():
                            write_list = ['VD', each_tec[0], key_measure, sum(vals) / len(vals)]
                            d.write(",".join([str(x) for x in write_list]))
                            d.write('\n')
                d.close()

                with open('app/static/results/comparison_result.csv') as csvfile:
                    r = DictReader(csvfile, skipinitialspace=True)
                    datam = [dict(d) for d in r]
                    # datam.pop(0)
                    # print(datam)

                    data = {}
                    for item in datam:
                        # print(item)
                        data.setdefault((item['d_metric'], item['c_method'], item['measure']), []).append(item['value'])
                    # print(data)
                    f = open('app/static/results/comparison_mean_result.csv', 'a')
                    for k, v in data.items():
                        # print(data.items())
                        ave = mean(float(n) if n else 0 for n in v)
                        write_list = [*k, ave]
                        f.write(",".join([str(x) for x in write_list]))
                        f.write('\n')
                    f.close()
            #
            else:
                print("No distance metric is selected")


            # print("I am done with DP")


        # with open('app/static/results/comparison_result.csv', 'r') as csvdata:
        #     next(csvdata, None)  # skip the headers
        #     reader = csv.DictReader(csvdata, fieldnames=['d_metric', 'c_method', 'c_ratio', 'measure', 'value'])
        #     json.dump([row for row in reader], open('app/static/results/comparison.json', 'w+'))
        #
        # return render_template("/public/Comparison.html", methods=method, json_result_url='/results/comparison.json')
        #

        #remove duplicates
        with open('app/static/results/comparison_mean_result.csv', 'r', newline='') as inputfile:
            with open('app/static/results/cleaned_comparison_mean_result.csv', 'w', newline='') as outputfile:
                duplicatereader = csv.DictReader(inputfile, delimiter=',')
                uniquewrite = csv.DictWriter(outputfile, fieldnames=['d_metric', 'c_method', 'measure', 'value'],
                                             delimiter=',')
                uniquewrite.writeheader()
                keysread = []
                for row in duplicatereader:
                    key = (row['d_metric'], row['c_method'], row['measure'])
                    if key not in keysread:
                        # print(row)
                        keysread.append(key)
                        uniquewrite.writerow(row)
            outputfile.close()
        inputfile.close()

        with open('app/static/results/cleaned_comparison_mean_result.csv') as csvfile:
            r = DictReader(csvfile, skipinitialspace=True)
            data = [dict(d) for d in r]

            groups = []
            uniquekeys = []

            for k, g in groupby(data, lambda r: (r['d_metric'], r['c_method'])):
                groups.append({
                    "d_metric": k[0],
                    "c_method": k[1],
                    "values": [
                        {k: v for k, v in d.items() if k not in ['d_metric', 'c_method']} for d
                        in list(g)]
                })
                uniquekeys.append(k)
        print(groups)

        # result = json.dumps((groups), open('app/static/results/comparison.json', 'w+')))
        # res = make_response(result, 200)
        with open('app/static/results/comparison_results.json', 'w') as f:
            json.dump(groups, f)
        return render_template("public/comparisonbarchart.html")

    else:

        print("data is not available")

    return redirect('/')

#
# @app.route('/checkit', methods=['POST'])
# def check_it_for_comparison():
#     methods = request.form.getlist('check')
#     dataset = request.form.get('data')
#     print(methods, dataset)
#     # Compress Ratio for PAA and DFT
#     ratios = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
#     result = dict()
#     compress_data =dict()
#
#     # Error tolerance for DP, VW and OPT
#     errors = [15, 25, 35, 50, 65, 80]
#     if os.path.exists('app/static/dataset/rawa_data/' + dataset + '.txt'):
#         data = open('app/static/dataset/rawa_data/' + dataset + '.txt', 'r')
#         print("compression started......")
#         dm = distance_metrics(dataset)
#         rawvolume = dm.raw_volfor1cluster()
#         # b=dm.raw_volfor1cluster()
#         print("raw volume calculated")
#         for datapoint in data:
#             # print("I am inside for loop")
#             datapoint = datapoint.split(',')
#             lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
#             if ((lon, lat) and (compression_method and compression_ratio)) not in compress_data:
#                 # print("I am inside if lat lon condition")
#                 print('Start dealing with ', str(lon), str(lat))
#                 time_series = [float(each_one) for each_one in datapoint[2:]]
#                 compress_data[(lon, lat)] = dict()
#                 compression_m_body = compression_method_body(time_series)
#                 c_tools = compress(time_series)
#
#                 compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.modify_vw(
#                     int(compression_ratio))
#             else:
#



@app.route('/visualize_TIN', methods=['POST'])
def visualize():

    if request.is_json:

        req = request.get_json()
        dataset = req.get("dataset")
        print(dataset)
        time = req.get("instance")
        compression_method = req.get("compression_method")
        compression_ratio = req.get("compression_ratio")
        method = req.get("method")
        raw_volume ={}

        #

        if os.path.exists('app/static/dataset/rawa_data/'+dataset+'.txt'):
            data = open('app/static/dataset/rawa_data/'+dataset+'.txt', 'r')
            print("compression started......")
            dm = distance_metrics(dataset)
            rawvolume = dm.raw_volfor1cluster()
            print("raw volume calculated")


def getdata():
    pass

def getStations(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, data):
    result_df = data[data['LAT'] >= topLeftLat]
    result_df = result_df[result_df['LAT'] <= bottomRightLat]
    result_df = result_df[result_df['LON'] <= topLeftLong]
    result_df = result_df[result_df['LON'] >= bottomRightLong]
    # select_dataset_range
    return result_df

# def getsingleStation():
#     subset_data = getStations(lat1, lon1, lat2, lon2, dataset2)
#     if len(subset_data) == 0:
#         print("Data is not available!")
#
#     print(subset_data)
#     subset_data_dict_show = subset_data.set_index('LAT')['LON'].to_dict()
#     print(subset_data_dict_show)
#     return result_df, subset_data


@app.route('/select_dataset_range', methods=["POST", "GET"])
def getsinglestation():
    dataset2 = pd.read_csv("app/static/dataset/rawa_data/myRes.csv", index_col=0)
    dataset2 = dataset2.fillna(0)
    if request.method == "GET":
        # table = request.args.get('selected_table')
        # print(table)
        # table = request.form['table1']
        print("=================================")
        lon1 = request.args.get('lon1')
        lat1 = request.args.get('lat1')
        lon2 = request.args.get('lon2')
        lat2 = request.args.get('lat2')
        subset_data = getStations(float(lat1), float(lon1), float(lat2), float(lon2), dataset2)
        if len(subset_data) == 0:
            print("Data is not available!")
            msg = "No data is available in the given range, please try again"
            return make_response(jsonify(msg), 200)

        # print(subset_data)
        with open("app/static/dataset/rawa_data/selected_subset.txt", 'w') as f:
            f.write(
                subset_data.to_csv(header=False, index=False, sep=',')
            )

        subset_data_dict_show = subset_data.set_index('LAT')['LON'].to_dict()
        # print(subset_data_dict_show)

        # print(lon1)
        #
        print("==================")
        # print(table)
        # attributes = request.args.get('attr')
        #
        # att = json.loads(attributes)
        # print(att)
        # print(len(attribu
        json_result = "pra"
        return make_response(jsonify(subset_data_dict_show))


@app.route('/predict', methods=['POST','GET'])
def prediction():

    methods1 = {
        'Discrete Fourier Transform (DFT)': [0.1, 0.15, 0.2, 0.25, 0.3, 0.5],
        'Piecewise Aggregate Approximation (PAA)': [0.1, 0.15, 0.2, 0.25, 0.3, 0.5],
        'Visvalingam-Whyatt Algorithm (VW)' : [15, 25, 35, 50, 65, 80],
        '(Adapted) Optimal Algorithm (OP)': [15, 25, 35, 50, 65, 80],
        '(Adapted) Douglas-Peucker Algorithm (DP)': [15, 25, 35, 50, 65, 80]
    }

    methods = {
        'Prophet Model': [2, 5, 7, 8, 10, 15, 20, 30, 40, 60, 75, 90],
        'Autoregressive Model': [2, 5, 7, 8, 10, 15, 20, 30, 40, 60, 75, 90],
        'ARIMA Model': [2, 5, 7, 8, 10, 15, 20, 30, 40, 60, 75, 90],
        'SARIMA Model': [2, 5, 7, 8, 10, 15, 20, 30, 40, 60, 75, 90]
    }



    return render_template("public/prediction.html", methods=methods, methods1=methods1)




@app.route("/prediction_results", methods=["POST", "GET"])
def input_prediction():

    # request.form.get

    # if compressed is False:
    dataset2 = pd.read_csv("app/static/dataset/rawa_data/myRes.csv", index_col=0)
    dataset2 = dataset2.fillna(0)

    # dataset2_compressed = pd.read_csv("app/static/dataset/rawa_data/myRes_compressed.csv", index_col=0)
    # function_1(lat1,lat2, lon1,lon2):
    #     dataset = "cluster1"
    #     return dataset
    #
    print('######################33333')
    # print(dataset2)
    print('######################33333')

    # print(c_method)
    # print(compression_ratio)

    # def getStations(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, data):
    #     result_df = data[data['LAT'] >= topLeftLat]
    #     result_df = result_df[result_df['LAT'] <= bottomRightLat]
    #     result_df = result_df[result_df['LON'] <= topLeftLong]
    #     result_df = result_df[result_df['LON'] >= bottomRightLong]
    #     return result_df
    lon1 = float(request.args.get("lon1"))
    # print(lon1)
    lat1 = float(request.args.get("lat1"))
    lon2 = float(request.args.get("lon2"))
    lat2 = float(request.args.get("lat2"))
    # print(lon1, lat1, lat2,lon2 )

    subset_data = getStations(lat1, lon1, lat2, lon2, dataset2)
    if len(subset_data) == 0:
        print("Data is not available!")
    #
    # print(subset_data)
    # subset_data_dict_show = subset_data.set_index('LAT')['LON'].to_dict()
    # print(subset_data_dict_show)
    # user selected form drop down menu

    station_name = request.args.get("subdata")
    # print(station_name)
    print("******************************************")

    spearte_station_lon_lat = station_name.split(',')
    # print(spearte_station_lon_lat)
    station_lat = spearte_station_lon_lat[0]
    station_lon = spearte_station_lon_lat[1]
    selected_station_lat = float(station_lat)
    selected_station_lon = float(station_lon)
    print("***********************************")
    prediction_method = request.args.get("method")
    prediction_window = int(request.args.get("day"))
    c_method = request.args.get("method1")
    compression_ratio = request.args.get("ratio1")
    print(c_method)
    print(compression_ratio)
    print("*****************************")
    # # lat = 78.250
    # # lon = 22.817

    def fix(user_input):
        mapping = {"Prophet Model": "PM", "Autoregressive Model": "AR",
                   "ARIMA Model": "ARIMA",
                   "SARIMA Model": "SARIMA",
                   }

        return mapping.get(user_input, user_input)

    def fix1(user_input):
        mapping = {"Discrete Fourier Transform (DFT)": "DFT", "Piecewise Aggregate Approximation (PAA)": "PAA",
                   "Visvalingam-Whyatt Algorithm (VW)": "VW", "(Adapted) Optimal Algorithm (OP)": "OP",
                    "(Adapted) Douglas-Peucker Algorithm (DP)": "DP"
                   }

        return mapping.get(user_input, user_input)


    # station_data = choose_a_station(subset_data)

    predict_method = fix(prediction_method)
    c_method = fix1(c_method)
    print(c_method)
    # p_data = pd.read_csv("app/static/dataset/rawa_data/myRes.csv")
    # data = pd.read_csv("app/static/dataset/rawa_data/myRes.csv")
    p_data = subset_data
    column_names = p_data.columns
    dates = column_names[3:]
    # print("############################")
    # print(p_data)
    temp_df = pd.DataFrame(columns=['date', 'temp'])
    ctemp_df = pd.DataFrame(columns=['date', 'temp'])

    temp_df['date'] = dates
    ctemp_df['date'] = dates
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    ctemp_df['date'] = pd.to_datetime(ctemp_df['date'])
    temperature = p_data[(p_data['LAT'] == selected_station_lat) & (p_data['LON'] == selected_station_lon)]
    print("!!!!!!!!!!!!!!!!!!!111")
    # print(temperature)
    print("!!!!!!!!!!!!!!!!!!!!!!")
    # print(temperature.iloc[0,1:].values)
    temperature_value = temperature.iloc[0, 3:].values
    # print(temperature_value)
    c_tools = compress(temperature_value)
    c_data = []
    d_metric = distance_metrics(ctemp_df)

    if c_method == "DFT":
        c_data = c_tools.dft(float(compression_ratio))

    elif c_method == "PAA":
        c_data = c_tools.paa(float(compression_ratio))

    elif c_method == "OP":
        c_data = c_tools.modify_opt(int(compression_ratio))
        c_data = d_metric.interpolate(c_data)

    elif c_method == "VW":
        c_data = c_tools.modify_vw(int(compression_ratio))
        c_data = d_metric.interpolate(c_data)

    elif c_method == "DP":
        c_data = c_tools.modify_dp(int(compression_ratio))
        c_data = d_metric.interpolate(c_data)

    else:
        print("method not defined")

    # c_data = c_tools.dft(float(0.01))
    # print(c_data)
    print("..................................=================")
    # print(c_data)
    print("..................................=================")
    temp_df['temp'] = temperature_value
    ctemp_df['temp'] = c_data
    temp_df = temp_df.rename(columns={'date': 'ds', 'temp': 'y'})
    ctemp_df = ctemp_df.rename(columns={'date': 'ds', 'temp': 'y'})

    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # # print(temp_df)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    p_model = predict_methods()

    if predict_method == "AR":

        p_model.AR_model(prediction_window, temp_df, name="AR")
        p_model.AR_model(prediction_window, ctemp_df, name="CAR")

        return render_template("public/prediction_results.html", method=prediction_method, p_window=prediction_window, file_name1='/images/prediction/{0}.png'.format(predict_method), file_name2='/images/prediction/CAR.png')

    elif predict_method == "PM":

        p_model.prophet_model(prediction_window, temp_df, name="PM")
        p_model.prophet_model(prediction_window, ctemp_df, name="CPM")


        return render_template("public/prediction_results.html", method=prediction_method,p_window=prediction_window, file_name1='/images/prediction/{0}.png'.format(predict_method),file_name2='/images/prediction/CPM.png')

    elif predict_method == "ARIMA":

        p_model.ARIMA_model(prediction_window, temp_df, name="ARIMA")
        p_model.ARIMA_model(prediction_window, ctemp_df, name="CARIMA")


        return render_template("public/prediction_results.html", method=prediction_method, p_window=prediction_window,
                               file_name1='/images/prediction/{0}.png'.format(predict_method), file_name2='/images/prediction/CARIMA.png')

    elif predict_method == "SARIMA":
        p_model.SARIMA(prediction_window, temp_df, name="SARIMA")
        p_model.SARIMA(prediction_window, ctemp_df, name="CSARIMA")

        return render_template("public/prediction_results.html", method=prediction_method, p_window=prediction_window,
                               file_name1='/images/prediction/{0}.png'.format(predict_method),
                               file_name2='/images/prediction/CSARIMA.png')

    else:
        return "No Method is selected"



        # return "I am okay for now with "+prediction_method+", prediction window of "+prediction_window+" days with location values "+lon+", "+lat

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_dataset', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template("public/upload.html")


@app.route('/select_sub_data', methods=["POST", "GET"])
def gettin_subdata():
    dataset2 = pd.read_csv("app/static/dataset/rawa_data/myRes.csv", index_col=0)
    dataset2 = dataset2.fillna(0)
    if request.method == "POST":
        # table = request.args.get('selected_table')
        # print(table)
        # table = request.form['table1']
        print("=================================")
        lon1 = request.form.get('lon1')
        lat1 = request.form.get('lat1')
        lon2 = request.form.get('lon2')
        lat2 = request.form.get('lat2')
        subset_data = getStations(float(lat1), float(lon1), float(lat2), float(lon2), dataset2)
        if len(subset_data) == 0:
            print("Data is not available!")
            msg = "No data is available in the given range, please try again"
            return make_response(jsonify(msg), 200)

        # print(subset_data)
        with open("app/static/dataset/rawa_data/selected_subset.txt", 'w') as f:
            f.write(
                subset_data.to_csv(header=False, index=False, sep=',')
            )



        # subset_data_dict_show = subset_data.set_index('LAT')['LON'].to_dict()
        # print(subset_data_dict_show)

        # print(lon1)
        #
        print("==================")
        msg = "Your subdata from selected range is created and available in dropdownmenus as selected_subset"
        # print(table)
        # attributes = request.args.get('attr')
        #
        # att = json.loads(attributes)
        # print(att)
        # print(len(attribu
        json_result = "pra"
        return make_response(jsonify(msg))
    return render_template("public/select_subdata.html")

@app.errorhandler(403)
def forbidden(e):
    return render_template("error_handlers/forbidden.html"), 403

@app.errorhandler(404)
def page_not_found(e):

    app.logger.info("Page not found: {0}".format(request.url))

    return render_template("error_handlers/404.html"), 404

@app.errorhandler(500)
def server_error(e):

    # email_admin(message="Server error", url=request.url, error=e)

    app.logger.error("Page not found: {0}".format(request.url))

    return render_template("error_handlers/500.html"), 500










