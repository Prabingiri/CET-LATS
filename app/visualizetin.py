import plotly.figure_factory as ff
from typing import Any, List, Dict, Union, Optional
import plotly.graph_objects as go
import plotly as ply
import time
import numpy as np
from scipy.spatial import Delaunay
import math
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

# from app.compress_nethods import compress
# from check_delaunay import distance_metrics

#
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

    return c_points



loc_time_series = dict()
rawdata = open('C:/Users/girip/PycharmProjects/CET-LATS/app/static/dataset/rawa_data/6.txt', 'r')
z = []
for dpoints in rawdata:
    dpoints = dpoints.split(',')
    lon, lat = lon_lat_to_XYZ(float(dpoints[0]), float(dpoints[1]))
    time_series = float(dpoints[2])
    z.append(time_series)
    loc_time_series[(lon, lat)] = time_series
points = np.array(list(loc_time_series.keys()))
a=points[:][:,0]
b=points[:][:,1]
# print(a)
# print(b)

values = np.array(z)

# points2D = np.vstack(points).T
tri = Delaunay((points))
simplices = tri.simplices

fig = ff.create_trisurf(x=a, y=b, z=values,
                         colormap="Portland",
                         simplices=simplices,
                         title="Tin visualization")
# fig.show()
# data = [fig]
fig.update_layout(
    title="TIN visualization",
    xaxis_title="lon",
    yaxis_title="lat",


)

ply.offline.plot(fig, filename='line-mode'+'.html')



from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import pyplot as plt
# dm = distance_metrics('cluster1')
compress_data = dict()
print("muji")
rdata = open('C:/Users/girip/PycharmProjects/CET-LATS/app/static/dataset/rawa_data/6.txt', 'r')
for datapoint in rdata:
    # print("I am inside for loop")
    datapoint = datapoint.split(',')
    lon, lat = lon_lat_to_XYZ(float(datapoint[0]), float(datapoint[1]))
    if ((lon, lat)) not in compress_data:
        # print("I am inside if lat lon condition")
        # print('Start dealing with ', str(lon), str(lat))
        time_series = [float(each_one) for each_one in datapoint[2:]]
        compress_data[(lon, lat)] = dict()
        # compression_m_body = compression_method_body(time_series)
        # c_tools = compress(time_series)

        compress_data[(lon, lat)] = paa(time_series, float(1))
        # print("data is compressed")
    # print(compress_data)
    # else:

        # print("I was already compressed ")
print(len(compress_data))
e= list(compress_data.values())

z2=[]
val_idx=0
for i in range(len(e)):
    z_m = e[i]
    z_val=z_m[val_idx]
    z2.append(z_val)
print((z2))
print(z)

# print(len(e[0][1]))
# z2=compress_data.keys()[0]
# print(z2)
import numpy as np

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# # colors = np.mean(CorticalImage[simplices], axis=1)
# collec = ax.plot_trisurf(a, b, z, triangles=simplices, cmap=cm.jet, linewidth=0.2)
# # collec.set_array(colors)
# collec.autoscale()
# ax.view_init(30, 0)
# cbar = fig.colorbar(collec)
# cbar.show()
fig = plt.figure(figsize=plt.figaspect(0.5))
tri = mtri.Triangulation(a, b)
ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.plot_trisurf(a, b, z2, triangles=tri.triangles, cmap=plt.cm.Spectral)
ax.set_title("After compression for the same instance")
ax.set_xlabel('longitude')
ax.set_ylabel('latitude')
ax.set_zlabel('values')
# m = cm.ScalarMappable(cmap=cm.Spectral)
# m.set_array(z2)
# plt.colorbar(m)
# ax.set_zlim(-1, 1)


# Create the Triangulation; no triangles so Delaunay triangulation created.
triang = mtri.Triangulation(a, b)

# Mask off unwanted triangles.
xmid = a[triang.triangles].mean(axis=1)
ymid = b[triang.triangles].mean(axis=1)
# mask = xmid**2 + ymid**2 < min_radius**2
# triang.set_mask(mask)

# Plot the surface.
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.plot_trisurf(triang, z, cmap=plt.cm.Spectral)
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
plt.show()

