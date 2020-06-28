
# import plotly.figure_factory as ff
from typing import Any, List, Dict, Union, Optional

import time
import numpy as np
from scipy.spatial import Delaunay
import math
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from simplification.cutil import simplify_coords_vw

from app.distance_metrics_final import distance_metrics
from app.compress_methods import compress


class visualize:
    # @staticmethod
    def __init__(self, dataset):
        # self.cd_data = dict()
        # pass
        self.dataset = dataset

    def sq_seg_dist(self, p1: float, pi: float, p2: float, i: int, first: int, last: int) -> float:
        """
        Square vertical distance between point and a segment
        """
        dx, dy = last - first, p2 - p1

        if not dx:
            ### dy == 0 because of time series data
            return (pi - p1) ** 2
        else:
            cy = (i - first) * (dy / dx) + p1
            return (pi - cy) ** 2

    def modify_dp(self, points, tolerance: int) -> List[float]:
        start = time.time()

        markers = [0 for _ in range(len(points))]

        first, last = 0, len(points) - 1

        first_stack, last_stack = [], []

        markers[first], markers[last] = 1, 1

        while last:
            max_sqdist, idx = -1, -1

            for i in range(first + 1, last):
                sq_dist = self.sq_seg_dist(points[i], points[first], points[last], i, first, last)
                # print(sq_dist)
                # print(max_sqdist)

                if sq_dist > max_sqdist:
                    idx = i
                    max_sqdist = sq_dist

            if max_sqdist > tolerance:
                markers[idx] = 1

                first_stack.append(first)
                last_stack.append(idx)

                first_stack.append(idx)
                last_stack.append(last)

            first = first_stack.pop() if first_stack else None

            last = last_stack.pop() if last_stack else None

        stop = time.time()
        c_points = [points[i] if markers[i] else None for i in range(len(markers))]
        # print(c_points)
        return c_points

    def modify_vw(self, points, tolerance: int) -> List[float]:
        start = time.time()
        list_param = [[idx, num] for idx, num in enumerate(points)]
        c_res = simplify_coords_vw(list_param, tolerance)

        stop = time.time()

        c_idx = 0
        c_points = []

        for idx in range(len(points)):
            if idx < c_res[c_idx][0]:
                c_points.append(None)
            elif idx == c_res[c_idx][0]:
                c_points.append(int(c_res[c_idx][1]))
                c_idx += 1
        # print((c_points))

        return c_points


    def dft(self, points, ratio: float) -> List[float]:
        start = time.time()
        l = math.floor(len(points) * ratio)

        markers = [1 for _ in range(len(points))]

        fts = np.fft.fft(points)

        while sum([1 if val else 0 for val in markers]) > l:
            min_square, min_idx = float("inf"), -1
            for idx in range(len(points)):
                if markers[idx] and fts[idx].real ** 2 + fts[idx].imag ** 2 < min_square:
                    min_idx, min_square = idx, fts[idx].real ** 2 + fts[idx].imag ** 2

            markers[min_idx] = None

        fts_0 = [fts[idx] if val else 0 + 0.j for idx, val in enumerate(markers)]

        c_points = np.fft.ifft(fts_0)

        stop = time.time()

        c_points = [val.real for val in c_points]

        return c_points


    def paa(self, points, ratio: float) -> List[float]:
        start = time.time()

        window_num = math.floor(len(points) * ratio)

        window_size = math.ceil(len(points) / window_num)

        c_points, idx = [0 for __ in points], 0

        while idx + window_size <= len(points):
            c_points[idx:idx + window_size] = [sum(points[idx:idx + window_size]) / window_size] * window_size
            idx += window_size

        if idx <= len(points) - 1:
            c_points[idx:] = [sum(points[idx:]) / len(points[idx:])] * len(points[idx:])
        # print(c_points)

        return c_points


    def circleALG(self, points, i: int, tolerance: int) -> List[int]:
        length = len(points)
        marker = [0 for _ in range(length)]

        marker[0], marker[i], marker[length - 1] = 1, 1, 1

        # Forward direction
        if i < length - 1:
            ratioH, ratioL = points[i + 1] + tolerance - points[i], points[i + 1] - tolerance - \
                             points[i]

            k = i + 2
            cur_idx = i

            while k <= length - 1:
                cur_rationH = (points[k] + tolerance - points[cur_idx]) / (k - cur_idx)
                cur_rationL = (points[k] - tolerance - points[cur_idx]) / (k - cur_idx)

                if cur_rationH < ratioL or cur_rationL > ratioH:
                    marker[k - 1], marker[k] = 1, 1
                    cur_idx = k
                    if k < length - 1:
                        ratioH, ratioL = points[k + 1] + tolerance - points[k], points[
                            k + 1] - tolerance - points[k]
                    k += 2
                else:
                    ratioH, ratioL = min(ratioH, cur_rationH), max(ratioL, cur_rationL)
                    k += 1

        # Backward Direction
        if i > 0:
            ratioH, ratioL = (points[i - 1] + tolerance - points[i]) / (-1), (
                    points[i - 1] - tolerance - points[i]) / (-1)

            j = i - 2
            cur_idx = i

            while j > 0:
                cur_rationH = (points[j] + tolerance - points[cur_idx]) / (j - cur_idx)
                cur_rationL = (points[j] - tolerance - points[cur_idx]) / (j - cur_idx)

                if cur_rationH > ratioL or cur_rationL < ratioH:
                    marker[j + 1], marker[j] = 1, 1
                    cur_idx = j
                    if j > 0:
                        ratioH, ratioL = (points[j] + tolerance - points[j - 1]) / (-1), (
                                points[j] - tolerance - points[j - 1]) / (-1)
                    j -= 2
                else:
                    ratioH, ratioL = max(ratioH, cur_rationH), min(ratioL, cur_rationL)
                    j -= 1

        return marker

    def modify_opt(self, points, tolerance: int) -> List[float]:
        start = time.time()
        c_marker = None
        for i in range(len(points)):
            marker = self.circleALG(points, i, tolerance)
            if (not c_marker) or sum(marker) < sum(c_marker):
                c_marker = marker

        stop = time.time()

        c_points = [points[i] if c_marker[i] else None for i in range(len(c_marker))]

        return c_points



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
        # print(points)

        return points

    def lon_lat_to_XYZ(self, lon: float, lat: float):
        # Convert angluar to cartesian coordiantes
        r = 6371  # https://en.wikipedia.org/wiki/Earth_radius
        theta = math.pi / 2 - math.radians(lat)
        phi = math.radians(lon)
        return r * math.sin(theta) * math.sin(phi), r * math.sin(theta) * math.cos(phi)

    def val_and_lon_lat(self, val_idx:int):
        loc_time_series = dict()
        rawdata = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + self.dataset + '.txt', 'r')

        # rawdata = open('/app/static/dataset/rawa_data/'+self.dataset+'.txt', 'r')
        # CET-LATS/app/static/dataset/rawa_data/6.txt
        z = []
        for dpoints in rawdata:
            dpoints = dpoints.split(',')
            lon, lat = self.lon_lat_to_XYZ(float(dpoints[0]), float(dpoints[1]))
            time_series = float(dpoints[val_idx])
            z.append(time_series)
            loc_time_series[(lon, lat)] = time_series
        points = np.array(list(loc_time_series.keys()))
        lon = points[:][:, 0]
        lat = points[:][:, 1]
        return lon, lat, z

    def compresse_interpolate(self, dataset, mthd, datatype, ratio):
        m = []
        rdata = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/' + self.dataset + '.txt', 'r')

        # rdata = open('app/static/dataset/rawa_data/'+dataset+'.txt', 'r')
        for datapoint in rdata:
            datapoint = datapoint.split(',')
            time_series = [float(each_one) for each_one in datapoint[2:]]
            h = mthd(time_series, datatype(ratio))
            f = self.interpolate(h)
            m.append(f)
        return m

    def interpolated_zvalue(self, val_idx, interpolated_points):
        z2 = []
        # val_idx = 0
        for i in range(len(interpolated_points)):
            z_m = interpolated_points[i]
            z_val = z_m[val_idx]
            z2.append(z_val)
        return z2

    def plotting(self, lon, lat, z_raw, z_compress, mthd, ratio):
        triang = mtri.Triangulation(lon, lat)
        fig = plt.figure(figsize=plt.figaspect(0.5))
        tri = mtri.Triangulation(lon, lat)
        ax = fig.add_subplot(1, 2, 2, projection='3d')
        ax.plot_trisurf(lon, lat, z_compress, triangles=tri.triangles, cmap=plt.cm.Spectral)
        ax.set_title("After compression for the same instance")
        ax.set_xlabel('longitude')
        ax.set_ylabel('latitude')
        ax.set_zlabel('values')
        # m = cm.ScalarMappable(cmap=cm.Spectral)
        # m.set_array(z2)
        # plt.colorbar(m)
        # ax.set_zlim(-1, 1)

        # Create the Triangulation; no triangles so Delaunay triangulation created.

        # Plot the surface.
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot_trisurf(triang, z_raw, cmap=plt.cm.Spectral)
        ax.set_title("Raw data in a single instance")
        ax.set_xlabel('longitude')
        ax.set_ylabel('latitude')
        ax.set_zlabel('values')
        # ax.legend(z)
        # plt.colorbar(ax=z)
        #
        m = plt.cm.ScalarMappable(cmap=plt.cm.Spectral)
        m.set_array(z_raw)
        plt.colorbar(m)
        # plt.show()
        return plt.savefig('app/static/images/TINinstance/3D{0}.png'.format(mthd.lower()))











