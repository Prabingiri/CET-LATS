from app import app
from flask import request, render_template, redirect
from flask import jsonify, make_response
# from app.distance_metrics import distance_metrics
from app.compress_methods import compress
from app.distance_metrics_final import distance_metrics
from app.visualization import visualize
import os
import csv
import json
import matplotlib.pyplot as plt
import matplotlib.tri as mtri




@app.route("/")
def index():
    return render_template("public/compare_methods.html")


@app.route("/input_values", methods=["POST"])
def input_comparision():

    if request.is_json:

        req = request.get_json()
        dataset = req.get("dataset")
        print(dataset)

        compression_method = req.get("compression_method")
        compression_ratio = req.get("compression_ratio")
        method = req.get("method")
        raw_volume ={}
        compress_data = dict()

        #

        if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')
            print("compression started......")
            dm = distance_metrics(dataset)
            rawvolume = dm.raw_volfor1cluster()
            print("raw volume calculated")

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
                    print(len(compress_data))

                    print(len(rawvolume))

                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method, compress_data)

                    print("compressed volume is calculated" )

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)
                    result3 = ad
                    print(result3)
                    result2 = hd
                    print("HD")
                    print(result2)
                    result1 = vol_diff
                    # resul =json.dumps(str(result1.items()))

                    voltlist = []
                    for key, value in result1.items():
                        temp = [key, value]
                        voltlist.append(temp)
                    value1 = (voltlist[0][1])

                    hdlist = []
                    for key, value in result2.items():
                        temp = [key, value]
                        hdlist.append(temp)
                    value2=(hdlist[0][1])

                    anglist = []
                    for key, value in result3.items():
                        temp = [key, value]
                        anglist.append(temp)
                    value3 = (anglist[0][1])

                    response_body = {

                        "Volumetric_difference": value1,
                        "Hausdarff_distance": value2,
                        "Angular_distance": value3,
                        "dataset": dataset,
                        "compression_ratio": compression_ratio,
                        "compression_method": compression_method,



                        }

                    res = make_response(jsonify(response_body), 200)
                    return res

            elif compression_method == "PAA":

                    print("I am inside PAA")
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

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.paa(float(compression_ratio))
                        else:

                            print("I was already compressed ")
                    print(len(compress_data))

                    print(len(rawvolume))

                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method, compress_data)

                    print("compressed volume is calculated" )

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd= dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)
                    result3 = ad
                    print(result3)
                    result2 = hd
                    print("HD")
                    print(result2)
                    result1 = vol_diff
                    # resul =json.dumps(str(result1.items()))

                    voltlist = []
                    for key, value in result1.items():
                        temp = [key, value]
                        voltlist.append(temp)
                    value1=(voltlist[0][1])

                    hdlist = []
                    for key, value in result2.items():
                        temp = [key, value]
                        hdlist.append(temp)
                    value2=(hdlist[0][1])

                    anglist = []
                    for key, value in result3.items():
                        temp = [key, value]
                        anglist.append(temp)
                    value3 = (anglist[0][1])

                    response_body = {

                        "Volumetric_difference": value1,
                        "Hausdarff_distance": value2,
                        "Angular_distance": value3,
                        "dataset": dataset,
                        "compression_ratio": compression_ratio,
                        "compression_method": compression_method,



                        }

                    res = make_response(jsonify(response_body), 200)
                    return res
            elif compression_method == "DP":

                    print("I am inside DP")
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

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.modify_dp(int(compression_ratio))

                    print("I was already compressed ")
                    print(len(compress_data))

                    print(len(rawvolume))

                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method, compress_data)

                    print("compressed volume is calculated" )

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd= dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)
                    result3 = ad
                    print(result3)
                    result2 = hd
                    print("HD")
                    print(result2)
                    result1 = vol_diff
                    # resul =json.dumps(str(result1.items()))

                    voltlist = []
                    for key, value in result1.items():
                        temp = [key, value]
                        voltlist.append(temp)
                    value1=(voltlist[0][1])

                    hdlist = []
                    for key, value in result2.items():
                        temp = [key, value]
                        hdlist.append(temp)
                    value2=(hdlist[0][1])

                    anglist = []
                    for key, value in result3.items():
                        temp = [key, value]
                        anglist.append(temp)
                    value3 = (anglist[0][1])

                    response_body = {
                        "dataset" : dataset,
                        "compression_method" : compression_method,
                        "compression_ratio": compression_ratio,
                        "Volumetric_difference": value1,
                        "Hausdarff_distance": value2,
                        "Angular_distance": value3


                        }

                    res = make_response(jsonify(response_body), 200)
                    return res


            elif compression_method == "VW":

                    print("I am inside VW")
                # self.compress_data[(lon, lat)] = dict()
                    for datapoint in data:
                        # print("I am inside for loop")
                        datapoint = datapoint.split(',')
                        lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
                        if ((lon, lat) and (compression_method and compression_ratio)) not in compress_data:
                            # print("I am inside if lat lon condition")
                            print('Start dealing with ', str(lon), str(lat))
                            time_series = [float(each_one) for each_one in datapoint[2:]]

                            c_tools = compress(time_series)

                            compress_data[(lon, lat)][(compression_method), compression_ratio] = c_tools.modify_vw(int(compression_ratio))
                        else:

                            print("I was already compressed ")
                    print(len(compress_data))

                    print(len(rawvolume))

                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method, compress_data)

                    print("compressed volume is calculated" )

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd= dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)
                    result3 = ad
                    print(result3)
                    result2 = hd
                    print("HD")
                    print(result2)
                    result1 = vol_diff
                    # resul =json.dumps(str(result1.items()))

                    voltlist = []
                    for key, value in result1.items():
                        temp = [key, value]
                        voltlist.append(temp)
                    value1=(voltlist[0][1])

                    hdlist = []
                    for key, value in result2.items():
                        temp = [key, value]
                        hdlist.append(temp)
                    value2=(hdlist[0][1])

                    anglist = []
                    for key, value in result3.items():
                        temp = [key, value]
                        anglist.append(temp)
                    value3 = (anglist[0][1])

                    response_body = {
                        "dataset" : dataset,
                        "compression_method" : compression_method,
                        "compression_ratio": compression_ratio,
                        "Volumetric_difference": value1,
                        "Hausdarff_distance": value2,
                        "Angular_distance": value3


                        }

                    res = make_response(jsonify(response_body), 200)
                    return res
            #
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
                    print(len(compress_data))

                    print(len(rawvolume))

                    compressedvolume = dm.compressed_volume(rawvolume, compression_ratio, compression_method, compress_data)

                    print("compressed volume is calculated" )

                    print("calculating volume difference")
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    hd= dm.Hausdarff_distance(rawvolume, compress_data)
                    ad = dm.Angular_diff(rawvolume, compress_data)
                    result3 = ad
                    print(result3)
                    result2 = hd
                    print("HD")
                    print(result2)
                    result1 = vol_diff
                    # resul =json.dumps(str(result1.items()))

                    voltlist = []
                    for key, value in result1.items():
                        temp = [key, value]
                        voltlist.append(temp)
                    value1 = (voltlist[0][1])

                    hdlist = []
                    for key, value in result2.items():
                        temp = [key, value]
                        hdlist.append(temp)
                    value2=(hdlist[0][1])

                    anglist = []
                    for key, value in result3.items():
                        temp = [key, value]
                        anglist.append(temp)
                    value3 = (anglist[0][1])

                    response_body = {
                        "dataset" : dataset,
                        "compression_method" : compression_method,
                        "compression_ratio": compression_ratio,
                        "Volumetric_difference": value1,
                        "Hausdarff_distance": value2,
                        "Angular_distance": value3


                        }

                    res = make_response(jsonify(response_body), 200)
                    return res


        else:
              return make_response(jsonify({"message": " Dataset is not available"}), 400)

    else:
        # print(compress_data)

        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


@app.route("/visualize")
def TIN_visualize():
    return render_template("public/visualization.html")

@app.route("/visualize_results", methods=["POST"])
def visualization():
    from app.visualization import visualize
    compression_method = request.form.get("compression")
    instance = request.form.get("s_instance")
    print(compression_method)
    print(instance)
    # data = open('app/static/dataset/rawa_data/cluster1.txt', 'r')

    dataset='6'
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
    return render_template("public/compare_methods.html")



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
    print(methods)
    dataset = request.form.get('data')
    # print(methods, dataset)
    # Compress Ratio for PAA and DFT
    ratios = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
    result = dict()
    ratios = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
    result = dict()

    # Error tolerance for DP, VW and OPT
    errors = [15, 25, 35, 50, 65, 80]
    if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
        # data = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + dataset + '.txt', 'r')
        print("compression started......")
        dm = distance_metrics(dataset)
        rawvolume = dm.raw_volfor1cluster()
        # b=dm.raw_volfor1cluster()
        print("raw volume calculated")
        method = set(methods)
        headers = ['d_metric', 'c_method', '1/c_ratio', 'measure', 'value']
        d = open('app/static/results/comparison_result.csv', 'w')
        w = csv.writer(d)
        w.writerow(headers)
        d.close()
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

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in hd.items():
                for key_measure, vals in mm.items():
                    write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))

                    # d.writerow(headers)
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in ad.items():
                for key_measure, vals in mm.items():
                    write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
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

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in hd.items():
                for key_measure, vals in mm.items():
                    write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in ad.items():
                for key_measure, vals in mm.items():
                    write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            for ratio in ratios:

                compressedvolume = dm.compressed_volume(rawvolume, ratio, 'PAA', compress_data)

                vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                for each_tec, mm in vol_diff.items():
                    for key_measure, vals in mm.items():
                        write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
            d.close()

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

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in hd.items():
                for key_measure, vals in mm.items():
                    write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in ad.items():
                for key_measure, vals in mm.items():
                    write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            for ratio in ratios:

                compressedvolume = dm.compressed_volume(rawvolume, ratio, 'DFT', compress_data)

                vol_diff = dm.volume_difference(rawvolume, compressedvolume)

                for each_tec, mm in vol_diff.items():
                    for key_measure, vals in mm.items():
                        write_list = ['VD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                        d.write(",".join([str(x) for x in write_list]))
                        d.write('\n')
            d.close()

            print("I am done with DFT")

        if 'OP' in method:
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
                        compress_data[(lon, lat)][('OP', error)] = c_tools.modify_opt(error)

            hd = dm.Hausdarff_distance(rawvolume, compress_data)
            ad = dm.Angular_diff(rawvolume, compress_data)

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in hd.items():
                for key_measure, vals in mm.items():
                    write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))

                    # d.writerow(headers)
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in ad.items():
                for key_measure, vals in mm.items():
                    write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
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
                        compress_data[(lon, lat)][('DP', error)] = c_tools.modify_dp(error)

            hd = dm.Hausdarff_distance(rawvolume, compress_data)
            ad = dm.Angular_diff(rawvolume, compress_data)

            d = open('app/static/results/comparison_result.csv', 'a')
            for each_tec, mm in hd.items():
                for key_measure, vals in mm.items():
                    write_list = ['HD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))

                    # d.writerow(headers)
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
            write_list = []
            for each_tec, mm in ad.items():
                for key_measure, vals in mm.items():
                    write_list = ['AD', each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
                    d.write(",".join([str(x) for x in write_list]))
                    d.write('\n')
            d.close()

            d = open('app/static/results/comparison_result.csv', 'a')
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


        with open('app/static/results/comparison_result.csv', 'r') as csvdata:
            next(csvdata, None)  # skip the headers
            reader = csv.DictReader(csvdata, fieldnames=['d_metric', 'c_method', 'c_ratio', 'measure', 'value'])
            json.dump([row for row in reader], open('app/static/results/comparison.json', 'w+'))

        return render_template("/public/Comparison.html", methods=method, json_result_url='/results/comparison.json')


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

        if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')
            print("compression started......")
            dm = distance_metrics(dataset)
            rawvolume = dm.raw_volfor1cluster()
            print("raw volume calculated")



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