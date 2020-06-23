from scipy.spatial import Delaunay
import math
import numpy as np
from typing import Any, List, Dict, Union, Optional
from scipy.spatial.distance import directed_hausdorff
import pickle
# import compressionmethods
# import distance_metr
# points = open('1.txt','rb')
class distance_metrics:
    def __init__(self, dataset):

        self.dataset = dataset
        # self.compress_data = compressdata
        # self.compress_data = compressionmethods.select_compressionmethod
        self.compressed_vol = dict()
        self.raw_volume = dict()
        self.whole_vol_res = dict()
        self.res_each_cluster = dict()
        self.loc_ts = dict()


    def preprocessing(self):

        for ts in self.rawdata:
            ts = ts.split(',')
            lon, lat = self.lon_lat_to_XYZ(float(ts[0]), float(ts[1]))
            time_s = [float(each_one) for each_one in ts[2:]]
            self.loc_ts[(lon, lat)] = time_s
        return self.loc_ts


    def interpolate(self, points: List[float]) -> List[float]:
        idx = 0

        while idx < len(points):
            if points[idx] is None:
                start_p = idx - 1
                while idx < len(points):
                    if points[idx] is not None:
                        break
                    idx += 1

                slope = (points[idx] - points[start_p]) / (idx - start_p)

                points[start_p + 1:idx] = [points[start_p] + i * slope for i in range(1, idx - start_p)]
            else:
                idx += 1

        return points


    def lon_lat_to_XYZ(self, lon: float, lat: float):
        # Convert angluar to cartesian coordiantes
        r = 6371  # https://en.wikipedia.org/wiki/Earth_radius
        theta = math.pi / 2 - math.radians(lat)
        phi = math.radians(lon)
        return r * math.sin(theta) * math.sin(phi), r * math.sin(theta) * math.cos(phi)

    def calc_Volume(self, p1, p2, p3):
        # print("calc_vol")
        base_area = 0.5 * abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
        h = 1 / 3 * (p1[2] + p2[2] + p3[2])
        volume = base_area * h
        return volume
    def raw_volfor1cluster(self):
        # raw_volume=dict()
        loc_time_series = dict()
        rawdata = open('app/static/dataset/rawa_data/'+self.dataset+ '.txt', 'r')
        for dpoints in rawdata:
            dpoints = dpoints.split(',')
            lon, lat = self.lon_lat_to_XYZ(float(dpoints[0]), float(dpoints[1]))
            time_series = [float(each_one) for each_one in dpoints[2:]]
            loc_time_series[(lon, lat)] = time_series
        points = np.array(list(loc_time_series.keys()))
        tris = Delaunay(points)
        # print(tris)
        for each_tri in points[tris.simplices]:
            p1, p2, p3 = tuple(each_tri[0]), tuple(each_tri[1]), tuple(each_tri[2])
            # print(p1, p2, p3)
            ts1, ts2, ts3 = loc_time_series[p1], loc_time_series[p2], loc_time_series[p3]
            # print(ts1, ts2, ts3)
            # print(len(ts1))
            # print(len(points))

            for timestamp in range(len(ts1)):
                self.raw_volume[(p1, p2, p3)] = self.raw_volume.get((p1, p2, p3), [])+\
                                           [self.calc_Volume(list(p1)+[ts1[timestamp]], list(p2)+[ts2[timestamp]], list(p3)+[ts3[timestamp]])]
        # print("the length is raw volume is:" )
        # print(lenself.raw_volume[165])
        rawdata.close()
        return self.raw_volume

       # f = open('app/static/dataset/rawa_data/'+dataset+ '.txt')
        # print("File exists:" + str(path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt')))
        # print(f)
        # if os.path.exists('app/static/dataset/rawa_data/'+dataset+ '.txt'):
    def compressed_volume(self, rawvolume, ratio, compress_data):

        compressed_vol=dict()
        for each_tri in rawvolume:
            # print("\n start compress vol \n")
            p1, p2, p3 = each_tri[0], each_tri[1], each_tri[2]
            # print(p1,p2,p3)
            compressed_vol[each_tri] = dict()

            # print(len(compress_data[p1][('dft', ratio)]))
            dft_ts_1 = compress_data[p1][('dft', ratio)]
            dft_ts_2 = compress_data[p2][('dft', ratio)]
            dft_ts_3 = compress_data[p3][('dft', ratio)]
            for tstamp in range(len(dft_ts_1)):
                compressed_vol[each_tri][('dft', ratio)] = \
                    compressed_vol[each_tri].get(('dft', ratio), []) + \
                    [self.calc_Volume(list(p1) + [dft_ts_1[tstamp]],
                             list(p2) + [dft_ts_2[tstamp]],
                             list(p3) + [dft_ts_3[tstamp]])]
        # # print("compressed_vol is : " )
        #     print("compressed vol completed")
            # print(len(compressed_vol))
        print(len(compressed_vol))
        return compressed_vol


    def volume_difference(self, raw_volume, compressed_vol):
        print("calculating difference")

        for each_tri in compressed_vol:
            print("still here")
            raw_vol = raw_volume[each_tri]
            res_each_cluster = dict()

            for c_tec, c_vol in compressed_vol[each_tri].items():
                min_diff, max_diff, mean_diff =\
                    min([abs(val - c_vol[idx]) for idx, val in enumerate(raw_vol)]), \
                    max([abs(val - c_vol[idx]) for idx, val in enumerate(raw_vol)]), \
                    sum([abs(val - c_vol[idx]) for idx, val in enumerate(raw_vol)])/len(raw_vol)


                if c_tec not in res_each_cluster:
                    res_each_cluster[c_tec] = {'min': [min_diff], 'max': [max_diff], 'mean': [mean_diff]}
                    print("finding min max")
                else:
                    res_each_cluster[c_tec]['min'].append(min_diff)
                    res_each_cluster[c_tec]['max'].append(max_diff)
                    res_each_cluster[c_tec]['mean'].append(mean_diff)
                    print("nearly done")



                print(" difference in volume is calculated")
                print(res_each_cluster)
                return res_each_cluster




    def Hausdarff_distance(self, raw_tri_vol, compress_data):
        print("xyz")
        whole_vol_res = dict()
        # infile = open('compress_data.pkl', 'rb')
        # compress_data = pickle.load(infile)
        # infile.close()
        #
        # infile = open('raw_tri_vol/' + data + '.pkl', 'rb')
        # raw_tri_vol = pickle.load(infile)
        # infile.close()
        #
        # data1 = open('cluster_data/' + data + '.txt',
        data = open('app/static/dataset/rawa_data/' + self.dataset + '.txt', 'r')
        loc_ts = dict()
        for ts in data:
            ts = ts.split(',')
            lon, lat = self.lon_lat_to_XYZ(float(ts[0]), float(ts[1]))
            time_s = [float(each_one) for each_one in ts[2:]]
            loc_ts[(lon, lat)] = time_s

        res_each_cluster = dict()

        for each_tri in raw_tri_vol:
            p1, p2, p3 = each_tri[0], each_tri[1], each_tri[2]
            raw1, raw2, raw3 = loc_ts[p1], loc_ts[p2], loc_ts[p3]

            for c_tech in compress_data[p1]:
                c1, c2, c3 = compress_data[p1][c_tech], compress_data[p2][c_tech], compress_data[p3][c_tech]
                if c_tech[0] == 'dp' or c_tech[0] == 'vw' or c_tech[0] == 'opt':
                    c_ratio = float(sum([1 if val is not None else 0 for val in c1]) +
                                    sum([1 if val is not None else 0 for val in c2]) +
                                    sum([1 if val is not None else 0 for val in c3])) / (3 * len(c1))
                    c1, c2, c3 = self.interpolate(c1), self.interpolate(c2), self.interpolate(c3)
                else:
                    c_ratio = c_tech[1]

                if (c_tech[0], c_ratio) not in res_each_cluster:
                    res_each_cluster[(c_tech[0], c_ratio)] = {'max': [], 'mean': [],'min': []}

                h_d = []
                for idx, val in enumerate(raw1):
                    raw_v = [(p1[0], p1[1], val), (p2[0], p2[1], raw2[idx]), (p3[0], p3[1], raw3[idx])]
                    c_v = [(p1[0], p1[1], c1[idx]), (p2[0], p2[1], c2[idx]), (p3[0], p3[1], c3[idx])]
                    h_d.append(max(directed_hausdorff(raw_v, c_v)[0], directed_hausdorff(c_v, raw_v)[0]))

                res_each_cluster[(c_tech[0], c_ratio)]['min'].append(min(h_d))
                res_each_cluster[(c_tech[0], c_ratio)]['max'].append(max(h_d))
                res_each_cluster[(c_tech[0], c_ratio)]['mean'].append(sum(h_d) / len(h_d))
            data.close()

            print("HD")
            return res_each_cluster

        # f = open('hd_res.txt', 'a')
        # f.write("Cluster " + data)
        # f.write('\n')

        # for each_tec, mmm in res_each_cluster.items():
        #     if each_tec not in whole_vol_res:
        #         whole_vol_res[each_tec] = {'max': [], 'mean': []}
        #     for key_meaure, vals in mmm.items():
        #         '''
        #         if key_meaure == 'min':
        #             write_list = [each_tec[0], each_tec[1], key_meaure, min(vals)]
        #             whole_vol_res[each_tec]['min'].append(min(vals))
        #             f.write(", ".join([str(x) for x in write_list]))
        #             f.write('\n')
        #         '''
        #         if key_meaure == 'max':
        #             write_list = [each_tec[0], each_tec[1], key_meaure, max(vals)]
        #             whole_vol_res[each_tec]['max'].append(max(vals))
        #             f.write(", ".join([str(x) for x in write_list]))
        #             f.write('\n')
        #         elif key_meaure == 'mean':
        #             write_list = [each_tec[0], each_tec[1], key_meaure, sum(vals) / len(vals)]
        #             whole_vol_res[each_tec]['mean'].append(sum(vals) / len(vals))
        #             f.write(", ".join([str(x) for x in write_list]))
        #             f.write('\n')
        #
        # print('Done with' + data + '/50')
        #
        # f = open('whole_hd_res.txt', 'a')
        # for each_tec, mmm in whole_vol_res.items():
        #     for key_measure, vals in mmm.items():
        #         write_list = [each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
        #         f.write(", ".join([str(x) for x in write_list]))
        #         f.write('\n')
        #
        # f.write('\n')


    def Angular_diff(self, raw_tri_vol, compress_data):
        print("Angular diff")
        whole_vol_res = dict()
        # infile = open('compress_data.pkl', 'rb')
        # compress_data = pickle.load(infile)
        # infile.close()
        # infile = open('raw_tri_vol/' + data + '.pkl', 'rb')
        # raw_tri_vol = pickle.load(infile)
        # infile.close()

        # f = open('cluster_data/' + data + '.txt', 'r')
        data = open('app/static/dataset/rawa_data/' + self.dataset + '.txt', 'r')
        loc_ts = dict()
        for ts in data:
            ts = ts.split(',')
            lon, lat = self.lon_lat_to_XYZ(float(ts[0]), float(ts[1]))
            time_s = [float(each_one) for each_one in ts[2:]]
            loc_ts[(lon, lat)] = time_s

        res_each_cluster = dict()

        for each_tri in raw_tri_vol:
            p1, p2, p3 = each_tri[0], each_tri[1], each_tri[2]
            raw1, raw2, raw3 = loc_ts[p1], loc_ts[p2], loc_ts[p3]

            for c_tech in compress_data[p1]:
                c1, c2, c3 = compress_data[p1][c_tech], compress_data[p2][c_tech], compress_data[p3][c_tech]
                if c_tech[0] == 'dp' or c_tech[0] == 'vw' or c_tech[0] == 'opt':
                    c_ratio = float(sum([1 if val is not None else 0 for val in c1]) +
                                    sum([1 if val is not None else 0 for val in c2]) +
                                    sum([1 if val is not None else 0 for val in c3])) / (3 * len(c1))
                    c1, c2, c3 = self.interpolate(c1), self.interpolate(c2), self.interpolate(c3)
                else:
                    c_ratio = c_tech[1]

                if (c_tech[0], c_ratio) not in res_each_cluster:
                    res_each_cluster[(c_tech[0], c_ratio)] = {'max': [], 'mean': [], 'min': []}

                h_d = []
                for idx in range(len(raw1)):
                    raw_p1, raw_p2, raw_p3 = np.array([p1[0], p1[1], raw1[idx]]), np.array(
                        [p2[0], p2[1], raw2[idx]]), \
                                             np.array([p3[0], p3[1], raw3[idx]])

                    raw_v1, raw_v2 = raw_p3 - raw_p1, raw_p2 - raw_p1

                    raw_normal_1, raw_normal_2, raw_normal_3 = np.cross(raw_v1, raw_v2)
                    raw_len = math.sqrt(raw_normal_1 * raw_normal_1 + raw_normal_2 * raw_normal_2 +
                                        raw_normal_3 * raw_normal_3)

                    c_p1, c_p2, c_p3 = np.array([p1[0], p1[1], c1[idx]]), np.array([p2[0], p2[1], c2[idx]]), \
                                       np.array([p3[0], p3[1], c3[idx]])

                    c_v1, c_v2 = c_p3 - c_p1, c_p2 - c_p1

                    c_normal_1, c_normal_2, c_normal_3 = np.cross(c_v1, c_v2)
                    c_len = math.sqrt(c_normal_1 * c_normal_1 + c_normal_2 * c_normal_2 +
                                      c_normal_3 * c_normal_3)

                    cs = max(-1.0, min(1.0, (raw_normal_1 * c_normal_1 + raw_normal_2 * c_normal_2 + raw_normal_3 *
                                             c_normal_3) / (raw_len * c_len)))

                    ##print(cs)

                    h_d.append(math.acos(cs) / math.pi)

                res_each_cluster[(c_tech[0], c_ratio)]['min'].append(min(h_d))
                res_each_cluster[(c_tech[0], c_ratio)]['max'].append(max(h_d))
                res_each_cluster[(c_tech[0], c_ratio)]['mean'].append(sum(h_d) / len(h_d))
            data.close()
            return res_each_cluster

        # f = open('angd_res.txt', 'a')
        # f.write("Cluster " + data)
        # f.write('\n')

        # for each_tec, mmm in res_each_cluster.items():
        #     if each_tec not in whole_vol_res:
        #         whole_vol_res[each_tec] = {'max': [], 'mean': []}
        #     for key_meaure, vals in mmm.items():
        #         '''
        #         if key_meaure == 'min':
        #             write_list = [each_tec[0], each_tec[1], key_meaure, min(vals)]
        #             whole_vol_res[each_tec]['min'].append(min(vals))
        #             f.write(", ".join([str(x) for x in write_list]))
        #             f.write('\n')
        #         '''
        #         if key_meaure == 'max':
        #             write_list = [each_tec[0], each_tec[1], key_meaure, max(vals)]
        #             whole_vol_res[each_tec]['max'].append(max(vals))
        #             f.write(", ".join([str(x) for x in write_list]))
        #             f.write('\n')
        #         elif key_meaure == 'mean':
        #             write_list = [each_tec[0], each_tec[1], key_meaure, sum(vals) / len(vals)]
        #             whole_vol_res[each_tec]['mean'].append(sum(vals) / len(vals))
        #             f.write(", ".join([str(x) for x in write_list]))
        #             f.write('\n')
        #
        # print('Done with' + data + '/50')
        #
        # f = open('whole_angd_res.txt', 'a')
        # for each_tec, mmm in whole_vol_res.items():
        #     for key_measure, vals in mmm.items():
        #         write_list = [each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
        #         f.write(", ".join([str(x) for x in write_list]))
        #         f.write('\n')
        #
        # f.write('\n')



    def mahanbolis_distance(self):
        print("xyz")


    #
    # def volume_difference_all(self, raw_volume, compressed_vol):
    #     print("calculating difference")
    #
    #     for each_tri in compressed_vol:
    #         print("still here")
    #         raw_vol = raw_volume[each_tri]
    #         res_each_cluster = dict()
    #
    #         for c_tec, c_vol in compressed_vol[each_tri].items():
    #             min_diff, max_diff, mean_diff = \
    #                 min([abs(val - c_vol[idx]) for idx, val in enumerate(raw_vol)]), \
    #                 max([abs(val - c_vol[idx]) for idx, val in enumerate(raw_vol)]), \
    #                 sum([abs(val - c_vol[idx]) for idx, val in enumerate(raw_vol)]) / len(raw_vol)
    #
    #             if c_tec not in res_each_cluster:
    #                 res_each_cluster[c_tec] = {'min': [min_diff], 'max': [max_diff], 'mean': [mean_diff]}
    #                 print("finding min max")
    #             else:
    #                 res_each_cluster[c_tec]['min'].append(min_diff)
    #                 res_each_cluster[c_tec]['max'].append(max_diff)
    #                 res_each_cluster[c_tec]['mean'].append(mean_diff)
    #                 print("nearly done")
    #
    #             print(" difference in volume is calculated")
    #             print(res_each_cluster)
    #             return res_each_cluster

# a=distance_metrics(points, None)
# # print(a.raw_volfor1cluster())
# b=a.raw_volfor1cluster()
# print(b)


# def angular_diff():
    # whole_vol_res = dict()
    # infile = open('compress_data.pkl', 'rb')
    # compress_data = pickle.load(infile)
    # infile.close()
    #
    # for i in range(1, 51):
    #     infile = open('raw_tri_vol/' + str(i) + '.pkl', 'rb')
    #     raw_tri_vol = pickle.load(infile)
    #     infile.close()
    #
    #     f = open('cluster_data/' + str(i) + '.txt', 'r')
    #     loc_ts = dict()
    #     for ts in f:
    #         ts = ts.split(',')
    #         lon, lat = lonlat_to_xyz(float(ts[0]), float(ts[1]))
    #         time_s = [float(each_one) for each_one in ts[2:]]
    #         loc_ts[(lon, lat)] = time_s
    #
    #     res_each_cluster = dict()
    #
    #     for each_tri in raw_tri_vol:
    #         p1, p2, p3 = each_tri[0], each_tri[1], each_tri[2]
    #         raw1, raw2, raw3 = loc_ts[p1], loc_ts[p2], loc_ts[p3]
    #
    #         for c_tech in compress_data[p1]:
    #             c1, c2, c3 = compress_data[p1][c_tech], compress_data[p2][c_tech], compress_data[p3][c_tech]
    #             if c_tech[0] == 'dp' or c_tech[0] == 'vw' or c_tech[0] == 'opt':
    #                 c_ratio = float(sum([1 if val is not None else 0 for val in c1]) +
    #                                 sum([1 if val is not None else 0 for val in c2]) +
    #                                 sum([1 if val is not None else 0 for val in c3])) / (3 * len(c1))
    #                 c1, c2, c3 = interpolate(c1), interpolate(c2), interpolate(c3)
    #             else:
    #                 c_ratio = c_tech[1]
    #
    #             if (c_tech[0], c_ratio) not in res_each_cluster:
    #                 res_each_cluster[(c_tech[0], c_ratio)] = {'max': [], 'mean': []}
    #
    #             h_d = []
    #             for idx in range(len(raw1)):
    #                 raw_p1, raw_p2, raw_p3 = np.array([p1[0], p1[1], raw1[idx]]), np.array([p2[0], p2[1], raw2[idx]]), \
    #                                          np.array([p3[0], p3[1], raw3[idx]])
    #
    #                 raw_v1, raw_v2 = raw_p3 - raw_p1, raw_p2 - raw_p1
    #
    #                 raw_normal_1, raw_normal_2, raw_normal_3 = np.cross(raw_v1, raw_v2)
    #                 raw_len = math.sqrt(raw_normal_1*raw_normal_1 + raw_normal_2 * raw_normal_2 +
    #                                     raw_normal_3 * raw_normal_3)
    #
    #                 c_p1, c_p2, c_p3 = np.array([p1[0], p1[1], c1[idx]]), np.array([p2[0], p2[1], c2[idx]]),\
    #                                    np.array([p3[0], p3[1], c3[idx]])
    #
    #                 c_v1, c_v2 = c_p3 - c_p1, c_p2 - c_p1
    #
    #                 c_normal_1, c_normal_2, c_normal_3 = np.cross(c_v1, c_v2)
    #                 c_len = math.sqrt(c_normal_1 * c_normal_1 + c_normal_2 * c_normal_2 +
    #                                   c_normal_3 * c_normal_3)
    #
    #                 cs = max(-1.0, min(1.0, (raw_normal_1 * c_normal_1 + raw_normal_2 * c_normal_2 + raw_normal_3 *
    #                                          c_normal_3)/(raw_len*c_len)))
    #
    #                 ##print(cs)
    #
    #                 h_d.append( math.acos(cs)/math.pi )
    #
    #
    #             # res_each_cluster[(c_tech[0], c_ratio)]['min'].append(min(h_d))
    #             res_each_cluster[(c_tech[0], c_ratio)]['max'].append(max(h_d))
    #             res_each_cluster[(c_tech[0], c_ratio)]['mean'].append(sum(h_d) / len(h_d))
    #
    #     f = open('angd_res.txt', 'a')
    #     f.write("Cluster " + str(i))
    #     f.write('\n')
    #
    #     for each_tec, mmm in res_each_cluster.items():
    #         if each_tec not in whole_vol_res:
    #             whole_vol_res[each_tec] = {'max': [], 'mean': []}
    #         for key_meaure, vals in mmm.items():
    #             '''
    #             if key_meaure == 'min':
    #                 write_list = [each_tec[0], each_tec[1], key_meaure, min(vals)]
    #                 whole_vol_res[each_tec]['min'].append(min(vals))
    #                 f.write(", ".join([str(x) for x in write_list]))
    #                 f.write('\n')
    #             '''
    #             if key_meaure == 'max':
    #                 write_list = [each_tec[0], each_tec[1], key_meaure, max(vals)]
    #                 whole_vol_res[each_tec]['max'].append(max(vals))
    #                 f.write(", ".join([str(x) for x in write_list]))
    #                 f.write('\n')
    #             elif key_meaure == 'mean':
    #                 write_list = [each_tec[0], each_tec[1], key_meaure, sum(vals) / len(vals)]
    #                 whole_vol_res[each_tec]['mean'].append(sum(vals) / len(vals))
    #                 f.write(", ".join([str(x) for x in write_list]))
    #                 f.write('\n')
    #
    #     print('Done with' + str(i) + '/50')
    #
    # f = open('whole_angd_res.txt', 'a')
    # for each_tec, mmm in whole_vol_res.items():
    #     for key_measure, vals in mmm.items():
    #         write_list = [each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
    #         f.write(", ".join([str(x) for x in write_list]))
    #         f.write('\n')
    #
    # f.write('\n')
    #



# def h_diff():
    # whole_vol_res = dict()
    # infile = open('compress_data.pkl', 'rb')
    # compress_data = pickle.load(infile)
    # infile.close()
    #
    # for i in range(1, 51):
    #     infile = open('raw_tri_vol/' + str(i) + '.pkl', 'rb')
    #     raw_tri_vol = pickle.load(infile)
    #     infile.close()
    #
    #     f = open('cluster_data/' + str(i) + '.txt', 'r')
    #     loc_ts = dict()
    #     for ts in f:
    #         ts = ts.split(',')
    #         lon, lat = lonlat_to_xyz(float(ts[0]), float(ts[1]))
    #         time_s = [float(each_one) for each_one in ts[2:]]
    #         loc_ts[(lon, lat)] = time_s
    #
    #     res_each_cluster = dict()
    #
    #     for each_tri in raw_tri_vol:
    #         p1, p2, p3 = each_tri[0], each_tri[1], each_tri[2]
    #         raw1, raw2, raw3 = loc_ts[p1], loc_ts[p2], loc_ts[p3]
    #
    #         for c_tech in compress_data[p1]:
    #             c1, c2, c3 = compress_data[p1][c_tech], compress_data[p2][c_tech], compress_data[p3][c_tech]
    #             if c_tech[0] == 'dp' or c_tech[0] == 'vw' or c_tech[0] == 'opt':
    #                 c_ratio = float(sum([1 if val is not None else 0 for val in c1]) +
    #                                 sum([1 if val is not None else 0 for val in c2]) +
    #                                 sum([1 if val is not None else 0 for val in c3])) / (3 * len(c1))
    #                 c1, c2, c3 = interpolate(c1), interpolate(c2), interpolate(c3)
    #             else:
    #                 c_ratio = c_tech[1]
    #
    #             if (c_tech[0], c_ratio) not in res_each_cluster:
    #                 res_each_cluster[(c_tech[0], c_ratio)] = {'max':[], 'mean':[]}
    #
    #             h_d = []
    #             for idx, val in enumerate(raw1):
    #                 raw_v = [(p1[0], p1[1], val), (p2[0], p2[1], raw2[idx]), (p3[0], p3[1], raw3[idx])]
    #                 c_v = [(p1[0], p1[1], c1[idx]), (p2[0], p2[1], c2[idx]), (p3[0], p3[1], c3[idx])]
    #                 h_d.append(max(directed_hausdorff(raw_v, c_v)[0], directed_hausdorff(c_v, raw_v)[0]))
    #
    #             #res_each_cluster[(c_tech[0], c_ratio)]['min'].append(min(h_d))
    #             res_each_cluster[(c_tech[0], c_ratio)]['max'].append(max(h_d))
    #             res_each_cluster[(c_tech[0], c_ratio)]['mean'].append(sum(h_d)/len(h_d))
    #
    #     f = open('hd_res.txt', 'a')
    #     f.write("Cluster " + str(i))
    #     f.write('\n')
    #
    #     for each_tec, mmm in res_each_cluster.items():
    #         if each_tec not in whole_vol_res:
    #             whole_vol_res[each_tec] = {'max': [], 'mean': []}
    #         for key_meaure, vals in mmm.items():
    #             '''
    #             if key_meaure == 'min':
    #                 write_list = [each_tec[0], each_tec[1], key_meaure, min(vals)]
    #                 whole_vol_res[each_tec]['min'].append(min(vals))
    #                 f.write(", ".join([str(x) for x in write_list]))
    #                 f.write('\n')
    #             '''
    #             if key_meaure == 'max':
    #                 write_list = [each_tec[0], each_tec[1], key_meaure, max(vals)]
    #                 whole_vol_res[each_tec]['max'].append(max(vals))
    #                 f.write(", ".join([str(x) for x in write_list]))
    #                 f.write('\n')
    #             elif key_meaure == 'mean':
    #                 write_list = [each_tec[0], each_tec[1], key_meaure, sum(vals) / len(vals)]
    #                 whole_vol_res[each_tec]['mean'].append(sum(vals) / len(vals))
    #                 f.write(", ".join([str(x) for x in write_list]))
    #                 f.write('\n')
    #
    #     print('Done with' + str(i) + '/50')
    #
    # f = open('whole_hd_res.txt', 'a')
    # for each_tec, mmm in whole_vol_res.items():
    #     for key_measure, vals in mmm.items():
    #         write_list = [each_tec[0], each_tec[1], key_measure, sum(vals) / len(vals)]
    #         f.write(", ".join([str(x) for x in write_list]))
    #         f.write('\n')
    #
    # f.write('\n')



