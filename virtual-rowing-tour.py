#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def kml2latlon(ifile):
    """Read lon lat from kml file with single path"""
    
    from fastkml import kml, geometry

    with open(ifile, 'rt') as myfile:
        doc = myfile.read()
    k = kml.KML()
    k.from_string(doc.encode("utf-8"))
    f = list(k.features())
    g = list(f[0].features())[0].geometry

    lat = []
    lon = []
    for c in g.coords:
        lon.append(c[0])
        lat.append(c[1])

    return lat, lon


def read_logbook(ifile, startdate=None, enddate=None):
    """ ToDo: Write reader for logbook to return distance in m
        rowed between start and end date"""
    
    import pandas

    df = pandas.read_csv('log/rowing.log',sep=' *; *')
    distance = df['meter'].sum(axis=0)
    last_date = df['date'].values[-1]
    print(last_date)
    print(distance)
    
    return distance, last_date


def coords2d(lat, lon):
    
    import shapely
    import numpy as np
    from cartopy import geodesic

    latlon = tuple(zip(lat, lon))
    myGeod = geodesic.Geodesic(6378137.0, 1/298.257223563)
    shapelyObject = shapely.geometry.LineString(list(latlon))
    s = myGeod.geometry_length(np.array(shapelyObject.coords))

    return s


def travel(distance, lat_route, lon_route):
    "ToDo: travel distance [m] along route and return position at destination"

    import shapely
    import numpy as np
    from cartopy import geodesic
    import sys
    import datetime

    # total length of route
    latlon = tuple(zip(lat_route, lon_route))
    myGeod = geodesic.Geodesic(6378137.0, 1 / 298.257223563)
    shapelyObject = shapely.geometry.LineString(list(latlon))
    # calculate length of path on ellipsoid
    s = myGeod.geometry_length(np.array(shapelyObject.coords))
    print("distance from start to finish is " + str(float(s)/1000.0) + " km")

    # distance to each waypoint
    s = 0.0
    s_vec = np.empty(len(lat_route))
    s_sum = np.empty(len(lat_route))
    s_vec[:] = np.NaN
    s_sum[:] = np.NaN
    for n in range(len(lat_route)):
        if n == 0:
            s = 0.0
            s_vec[n] = s
            s_sum[n] = s
        else:
            # row leg from waypoint n-1 to n
            s = coords2d([lat_route[n-1], lat_route[n]],
                         [lon_route[n-1], lon_route[n]])
            s_vec[n] = s
            s_sum[n] = s + s_sum[n-1]
        # print(n)
        # print(s_vec[n])
        # print(s_sum[n])
        # print ("----")
        
    # Find last passed waypoint
    lat_pos = lat_route[0]
    lon_pos = lon_route[0]
    for n in range(len(s_sum)):
        if s_sum[n] > distance:
            lat_pos = lat_route[n-1]
            lon_pos = lon_route[n-1]
            # distance traveled from last know position
            res = distance - s_sum[n-1]
            # print(n)
            # print(res)
            # print(distance)
            break
            
    # ToDo: Correct position by travelling the distance res
    #       from the last know position (lat_pos, lon_pps) 

    # ToDo: Quality control (Check if parameters for geoid are consitent
    #       with google earth, try different routes, ...)

    return lat_pos, lon_pos


def main():

    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    # Define start and finish

    name_start = "Exmouth"
    name_finish = "La Gomera"

    # read planned route from kml file

    ifile_kml = "routes/route.kml"
    # ifile_kml = "routes/shortcut.kml"

    lat_route, lon_route = kml2latlon(ifile_kml)

    distance, last_date = read_logbook("log/rowing.log",
                                       startdate="2020-10-31",
                                       enddate="2020-10-31")

    # Define position of boat
    
    lat_boat, lon_boat = travel(distance, lat_route, lon_route)

    # Create plot

    extent1 = [-20, 2.5, 25, 52.5]
    extent2 = [-6, -2.5, 47.5, 51]

    fig = plt.figure(figsize=(10, 8))
    fig.suptitle('Exmouth to La Gomera ' + last_date)

    rivers_10m = cfeature.NaturalEarthFeature('physical',
                                              'rivers_lake_centerlines', '10m')
    land_10m = cfeature.NaturalEarthFeature('physical',
                                            'land', '10m',
                                            edgecolor='face',
                                            facecolor=cfeature.COLORS['land'])

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()

    ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax1.set_extent(extent1, crs=ccrs.PlateCarree())
    # ax1.coastlines(resolution='50m')
    ax1.add_feature(land_10m)
    # ax1.add_feature(rivers_10m, facecolor='None', edgecolor='b', alpha=0.5)
    ax1.set_xticks([-20, -15, -10, -5, 0, 5])
    ax1.xaxis.set_major_formatter(lon_formatter)
    ax1.set_yticks([25, 30, 35, 40, 45, 50])
    ax1.yaxis.set_major_formatter(lat_formatter)
    ax1.plot(lon_route[0], lat_route[0], marker='o', color='blue',
             markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax1.plot(lon_route[-1], lon_route[-1], marker='o', color='blue',
             markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax1.plot(lon_route, lat_route, ':', transform=ccrs.PlateCarree())
    ax1.plot(lon_boat, lat_boat, marker='o', color='red',
             markersize=8, alpha=0.7, transform=ccrs.PlateCarree())
    ax1.set_title('Expedition chart')

    ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())
    ax2.add_feature(land_10m)
    ax2.set_xticks([-20, -15, -10, -5, 0, 5])
    ax2.xaxis.set_major_formatter(lon_formatter)
    ax2.set_yticks([25, 30, 35, 40, 45, 50])
    ax2.yaxis.set_major_formatter(lat_formatter)
    ax2.plot(lon_route[0], lon_route[0], marker='o', color='blue',
             markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax2.plot(lon_route[-1], lon_route[-1], marker='o', color='blue',
             markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax2.plot(lon_route, lat_route, ':', transform=ccrs.PlateCarree())
    ax2.plot(lon_boat, lat_boat, marker='o', color='red',
             markersize=8, alpha=0.7, transform=ccrs.PlateCarree())
    ax2.set_title('Chart of the day')
    ax2.set_extent(extent2)

    plt.show()
    #plt.savefig("plots/Exmouth_RC_virtual_row_winter_2020--2021.png")


if __name__ == "__main__":
    main()