from app import app
from flask import request, render_template, redirect
from flask import jsonify, make_response
# from app.distance_metrics import distance_metrics
from app.compress_methods import compress
from app.distance_metrics_final import distance_metrics
import os




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
                            compression_m_body = compression_method_body(time_series)
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
                            compression_m_body = compression_method_body(time_series)
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


@app.route("/compare_compression", methods=["POST"])
def compare_methods():
    if request.is_json:

        req = request.get_json()
        dataset = req.get("dataset")
        print(dataset)

        # compression_method = req.get("compression_method")
        # compression_ratio = req.get("compression_ratio")
        # method = req.get("method")
        raw_volume ={}
        methods = req.POST.get("methods")

        #

        if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
            data = open('app/static/dataset/rawa_data/'+dataset+ '.txt', 'r')
            print("compression started......")
            dm = distance_metrics(dataset)
            rawvolume = dm.raw_volfor1cluster()
            print("raw volume calculated")


            for mthod in methods:
                if mthod == "DFT":
                  print("I might work")


@app.route("/TIN_visualization", methods=["POST"])
def TIN_visualization():
    print("TINS are visualizaed")
#
# @app.route("/input_values", methods=["POST"])
# def input_comparision():

@app.route('/user_rec', methods=['POST'])
def user_rec():
    # user_name = request.form.get('user_input')
    # min_time = request.form.get('min_time')
    # max_time = request.form.get('max_time')
    # compress_data=dict()
    methods = request.form.getlist('check')
    dataset = request.form.get('data')
    print(methods, dataset)
    # Compress Ratio for PAA and DFT
    ratios = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]
    result = dict()

    # Error tolerance for DP, VW and OPT
    errors = [15, 25, 35, 50, 65, 80]
    if os.path.exists('app/static/dataset/rawa_data/' + dataset + '.txt'):
        data = open('app/static/dataset/rawa_data/' + dataset + '.txt', 'r')
        print("compression started......")
        dm = distance_metrics(dataset)
        rawvolume = dm.raw_volfor1cluster()
        # b=dm.raw_volfor1cluster()
        print("raw volume calculated")

        for mthd in methods:

            if mthd == "DFT":
                compress_data = dict()
                for datapoint in data:
                    # print("I am inside for loop")
                    datapoint = datapoint.split(',')
                    lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

                    if (lon, lat) and mthd not in compress_data:
                            # print("Bhawana")
                        print('Start dealing with ', str(lon), str(lat))
                        time_series = [float(each_one) for each_one in datapoint[2:]]
                        compress_data[(lon, lat)] = dict()
                        # compression_m_body = compression_method_body(time_series)
                        c_tools = compress(time_series)
                        for ratio in ratios:
                            compress_data[(lon, lat)][(mthd, ratio)] = c_tools.dft(ratio)
                    # print("I was already compressed ")
                    # print(len(compress_data))

                    # print(len(rawvolume))
                vol_dif = []
                hd_dif = []
                ag_dif = []
                for ratio in ratios:
                    compressedvolume = dm.compressed_volume(rawvolume, ratio, mthd, compress_data)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    vol_dif.append(vol_diff)
                    # hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    # hd_dif.append(hd)
                    # ad = dm.Angular_diff(rawvolume, compress_data)
                    # ag_dif.append(ad)
                hd = dm.Hausdarff_distance(rawvolume, compress_data)
                ad = dm.Angular_diff(rawvolume, compress_data)
                # print(vol_diff)
                print(hd.values())
                print(ad.values())
                # hd= dm.Hausdarff_distance(rawvolume, compress_data)
                # ad = dm.Angular_diff(rawvolume, compress_data)
                # print((compress_data))
                print("I am done with DFT" )
                # return vol_dif, hd, ad

            elif mthd == "PAA":
                c_data = dict()
                for datapoint in data:
                    # print("I am inside for loop")
                    datapoint = datapoint.split(',')
                    lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

                    if (lon, lat) and mthd not in c_data:
                            # print("Bhawana")
                        print('Start dealing with ', str(lon), str(lat))
                        time_series = [float(each_one) for each_one in datapoint[2:]]
                        c_data[(lon, lat)] = dict()
                        # compression_m_body = compression_method_body(time_series)
                        c_tools = compress(time_series)
                        for ratio in ratios:
                            c_data[(lon, lat)][(mthd, ratio)] = c_tools.paa(ratio)
                    # print("I was already compressed ")
                    # print(len(compress_data))

                    # print(len(rawvolume))
                vol_dif = []
                hd_dif = []
                ag_dif = []
                for ratio in ratios:
                    compressedvolume = dm.compressed_volume(rawvolume, ratio, mthd, c_data)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    vol_dif.append(vol_diff)
                    # hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    # hd_dif.append(hd)
                    # ad = dm.Angular_diff(rawvolume, compress_data)
                    # ag_dif.append(ad)
                hd = dm.Hausdarff_distance(rawvolume, c_data)
                ad = dm.Angular_diff(rawvolume, c_data)
                # print(vol_diff)
                print(hd.values())
                print(ad.values())
                # hd= dm.Hausdarff_distance(rawvolume, compress_data)
                # ad = dm.Angular_diff(rawvolume, compress_data)
                # print((compress_data))
                print("I am done with PAA" )
                # return vol_dif, hd, ad
            elif mthd == "DP":
                compress_data = dict()
                for datapoint in data:
                    # print("I am inside for loop")
                    datapoint = datapoint.split(',')
                    lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

                    if (lon, lat) and mthd not in compress_data:

                        print('Start dealing with ', str(lon), str(lat))
                        time_series = [float(each_one) for each_one in datapoint[2:]]
                        compress_data[(lon, lat)] = dict()
                        # compression_m_body = compression_method_body(time_series)
                        c_tools = compress(time_series)
                        for error in errors:
                            compress_data[(lon, lat)][(mthd, error)] = c_tools.modify_dp(error)
                    # print("I was already compressed ")
                    # print(len(compress_data))

                    # print(len(rawvolume))
                vol_dif = []
                hd_dif = []
                ag_dif = []
                for error in errors:
                    compressedvolume = dm.compressed_volume(rawvolume, error, mthd, compress_data)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    vol_dif.append(vol_diff)
                    # hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    # hd_dif.append(hd)
                    # ad = dm.Angular_diff(rawvolume, compress_data)
                    # ag_dif.append(ad)
                hd = dm.Hausdarff_distance(rawvolume, compress_data)
                ad = dm.Angular_diff(rawvolume, compress_data)
                # print(vol_diff)
                print(hd.values())
                print(ad.values())
                # hd= dm.Hausdarff_distance(rawvolume, compress_data)
                # ad = dm.Angular_diff(rawvolume, compress_data)
                # print((compress_data))
                print("I am done with DP" )
                # return vol_dif, hd, ad
            elif mthd == "VW":
                compress_data = dict()
                for datapoint in data:
                    # print("I am inside for loop")
                    datapoint = datapoint.split(',')
                    lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

                    if ((lon, lat) and mthd) not in compress_data:
                            # print("Bhawana")
                        print('Start dealing with ', str(lon), str(lat))
                        time_series = [float(each_one) for each_one in datapoint[2:]]
                        compress_data[(lon, lat)] = dict()
                        # compression_m_body = compression_method_body(time_series)
                        c_tools = compress(time_series)
                        for error in errors:
                            compress_data[(lon, lat)][(mthd, error)] = c_tools.modify_vw(error)
                    # print("I was already compressed ")
                    # print(len(compress_data))

                    # print(len(rawvolume))
                vol_dif = []
                hd_dif = []
                ag_dif = []
                for error in errors:
                    compressedvolume = dm.compressed_volume(rawvolume, error, mthd, compress_data)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    vol_dif.append(vol_diff)
                    # hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    # hd_dif.append(hd)
                    # ad = dm.Angular_diff(rawvolume, compress_data)
                    # ag_dif.append(ad)

                hd = dm.Hausdarff_distance(rawvolume, compress_data)
                ad = dm.Angular_diff(rawvolume, compress_data)
                print("vol_diff")
                print(vol_dif)
                print("hd")
                print(hd)
                print("ad")
                print(ad)
                # hd= dm.Hausdarff_distance(rawvolume, compress_data)
                # ad = dm.Angular_diff(rawvolume, compress_data)
                # print((compress_data))
                print("I am done with VW" )
                # return vol_dif, hd, ad

            elif mthd == "OP":
                compress_data = dict()
                for datapoint in data:
                    # print("I am inside for loop")
                    datapoint = datapoint.split(',')
                    lon, lat = dm.lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))

                    if (lon, lat) and mthd not in compress_data:

                        print('Start dealing with ', str(lon), str(lat))
                        time_series = [float(each_one) for each_one in datapoint[2:]]
                        compress_data[(lon, lat)] = dict()
                        # compression_m_body = compression_method_body(time_series)
                        c_tools = compress(time_series)
                        for error in errors:
                            compress_data[(lon, lat)][(mthd, error)] = c_tools.modify_opt(error)

                vol_dif = []
                hd_dif = []
                ag_dif = []
                for error in errors:
                    compressedvolume = dm.compressed_volume(rawvolume, error, mthd, compress_data)
                    vol_diff = dm.volume_difference(rawvolume, compressedvolume)
                    vol_dif.append(vol_diff)
                    # hd = dm.Hausdarff_distance(rawvolume, compress_data)
                    # hd_dif.append(hd)
                    # ad = dm.Angular_diff(rawvolume, compress_data)
                    # ag_dif.append(ad)
                hd = dm.Hausdarff_distance(rawvolume, compress_data)
                ad = dm.Angular_diff(rawvolume, compress_data)
                # print(vol_diff)
                print(hd.values())
                print(ad.values())
                # hd= dm.Hausdarff_distance(rawvolume, compress_data)
                # ad = dm.Angular_diff(rawvolume, compress_data)
                # print((compress_data))
                print("I am done with DFT" )
                # return vol_dif, hd, ad


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