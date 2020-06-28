
from typing import Any, List, Dict, Union, Optional
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from simplification.cutil import simplify_coords_vw

# from app.compress_nethods import compress
# from check_delaunay import distance_metrics

#


def sq_seg_dist(p1: float, pi: float, p2: float, i: int, first: int, last: int) -> float:
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


def modify_dp(points, tolerance: int) -> List[float]:
    start = time.time()

    markers = [0 for _ in range(len(points))]

    first, last = 0, len(points) - 1

    first_stack, last_stack = [], []

    markers[first], markers[last] = 1, 1

    while last:
        max_sqdist, idx = -1, -1

        for i in range(first + 1, last):
            sq_dist = sq_seg_dist(points[i], points[first], points[last], i, first, last)
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

def modify_vw(points, tolerance: int) -> List[float]:
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

def interpolate(points: List[float]) -> List[float]:
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

def lon_lat_to_XYZ(lon: float, lat: float):
    # Convert angluar to cartesian coordiantes
    r = 6371  # https://en.wikipedia.org/wiki/Earth_radius
    theta = math.pi / 2 - math.radians(lat)
    phi = math.radians(lon)
    return r * math.sin(theta) * math.sin(phi), r * math.sin(theta) * math.cos(phi)

def paa(points, ratio: float) -> List[float]:
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



# loc_time_series = dict()
# rawdata = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/6.txt', 'r')
# # CET-LATS/app/static/dataset/rawa_data/6.txt
# z = []
# for dpoints in rawdata:
#     dpoints = dpoints.split(',')
#     lon, lat = lon_lat_to_XYZ(float(dpoints[0]), float(dpoints[1]))
#     time_series = float(dpoints[2])
#     z.append(time_series)
#     loc_time_series[(lon, lat)] = time_series
# points = np.array(list(loc_time_series.keys()))
# lon = points[:][:,0]
# lat = points[:][:,1]
#
# m=[]
# n=[]
# rdata = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/6.txt', 'r')
# for datapoint in rdata:
#     datapoint = datapoint.split(',')
#     time_series = [float(each_one) for each_one in datapoint[2:]]
#     h = paa(time_series, float(0.5))
#     f = interpolate(h)
#     m.append(f)
#

# print(m)
# z2 = []
# val_idx = 0
# for i in range(len(m)):
#     z_m = m[i]
#     z_val = z_m[val_idx]
#     z2.append(z_val)
# # print("hahaha")
# print(z2)
# print(z)


# fig = plt.figure()
# ax = fig.gca(projection='3d')
# # colors = np.mean(CorticalImage[simplices], axis=1)
# collec = ax.plot_trisurf(a, b, z, triangles=simplices, cmap=cm.jet, linewidth=0.2)
# # collec.set_array(colors)
# collec.autoscale()
# ax.view_init(30, 0)
# cbar = fig.colorbar(collec)
# cbar.show()
# fig = plt.figure(figsize=plt.figaspect(0.5))
# tri = mtri.Triangulation(a, b)
# ax = fig.add_subplot(1, 2, 2, projection='3d')
# ax.plot_trisurf(a, b, z2, triangles=tri.triangles, cmap=plt.cm.Spectral)
# ax.set_title("After compression for the same instance")
# ax.set_xlabel('longitude')
# ax.set_ylabel('latitude')
# ax.set_zlabel('values')
# # m = cm.ScalarMappable(cmap=cm.Spectral)
# # m.set_array(z2)
# # plt.colorbar(m)
# # ax.set_zlim(-1, 1)
#
#
# # Create the Triangulation; no triangles so Delaunay triangulation created.
# triang = mtri.Triangulation(a, b)
#
#
# # Plot the surface.
# ax = fig.add_subplot(1, 2, 1, projection='3d')
# ax.plot_trisurf(triang, z, cmap=plt.cm.Spectral)
# ax.set_title("Raw data in a single instance")
# ax.set_xlabel('longitude')
# ax.set_ylabel('latitude')
# ax.set_zlabel('values')
# # ax.legend(z)
# # plt.colorbar(ax=z)
# #
# # m = cm.ScalarMappable(cmap=cm.Spectral)
# # m.set_array(z)
# # plt.colorbar(m)
# plt.show()
#

def val_and_lon_lat(val_idx, dataset):
    loc_time_series = dict()
    rawdata = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/'+dataset+'.txt', 'r')
    # CET-LATS/app/static/dataset/rawa_data/6.txt
    z = []
    for dpoints in rawdata:
        dpoints = dpoints.split(',')
        lon, lat = lon_lat_to_XYZ(float(dpoints[0]), float(dpoints[1]))
        time_series = float(dpoints[val_idx])
        z.append(time_series)
        loc_time_series[(lon, lat)] = time_series
    points = np.array(list(loc_time_series.keys()))
    lon = points[:][:, 0]
    lat = points[:][:, 1]
    return lon, lat, z


def compresse_interpolate(dataset, mthd, datatype):
    m = []
    n = []
    rdata = open('/home/prabin/Sigspatial2020/CET-LATS/app/static/dataset/rawa_data/'+dataset+'.txt', 'r')
    for datapoint in rdata:
        datapoint = datapoint.split(',')
        time_series = [float(each_one) for each_one in datapoint[2:]]
        h = mthd(time_series, datatype(0.5))
        f = interpolate(h)
        m.append(f)
    return m


def interpolated_zvalue(val_idx, interpolated_points):
    z2 = []
    # val_idx = 0
    for i in range(len(interpolated_points)):
        z_m = interpolated_points[i]
        z_val = z_m[val_idx]
        z2.append(z_val)
    return z2

def plotting(lon, lat, z_raw, z_compress, mthd, ratio):
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
    # m = cm.ScalarMappable(cmap=cm.Spectral)
    # m.set_array(z)
    # plt.colorbar(m)
    # plt.show()
    plt.savefig("3D__{0}".format(mthd))
    return fig


# val_idx = 0
# ratio = 0.5
# # mthd=DFT
# lon, lat, z = val_and_lon_lat(val_idx=val_idx, dataset='6')
# print(z)
# cm_points = compresse_interpolate(dataset='6', mthd=paa, datatype=float)
# z2 = interpolated_zvalue(val_idx=0,interpolated_points = cm_points)
# print(z2)
#
# plotting(lon=lon, lat=lat, z_raw=z, z_compress=z2, mthd='paa', ratio=ratio)
from app.visualization import visualize
v = visualize('6')
# # visual.plotting()
val_idx = 2
ratio = 0.5
# # mthd=DFT
lon, lat, z = v.val_and_lon_lat(val_idx=val_idx+2)
print(z)
cm_points = v.compresse_interpolate(dataset='6', mthd=v.dft, datatype=float)
z2 = v.interpolated_zvalue(val_idx=0,interpolated_points = cm_points)
print(z2)
print('Prabin')
#
