#!/usr/bin/env python3
# -*- coding: utf-8 -*-

        
def main():

    import cartopy.crs as ccrs
    import cartopy
    import cartopy.feature as cfeature
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    from cartopy.io.img_tiles import StamenTerrain
    import numpy as np
    import matplotlib.pyplot as plt
    import shapely
    import sys
    from fastkml import kml, geometry 

    # Define start and finish
    
    lat_exmouth = 50.62
    lon_exmouth = -3.4137

    lat_la_gomera = 28.1033 
    lon_la_gomera = -17.2194
    
    # read planned route from kml file
        
    ifile_kml = "route.kml"    
    with open(ifile_kml, 'rt', encoding="utf-8") as myfile:
        doc = myfile.read()
    k = kml.KML()
    k.from_string(doc.encode('utf-8'))
    features = list(k.features())
    f2 = list(features[0].features())
    g = f2[0].geometry
    lon_route = []
    lat_route = []
    for c in g.coords:
        lon_route.append(c[0])
        lat_route.append(c[1])

    lon_route.append(lon_la_gomera)
    lat_route.append(lat_la_gomera)

    # Define position of boat
    
    lat_boat=lat_exmouth
    lon_boat=lon_exmouth

    # Create plot
    
    extent1 = [-20, 2.5, 25, 52.5]
    extent2 = [-6, -2.5, 47.5, 51]

    fig = plt.figure(figsize=(10, 8))
    fig.suptitle('Exmouth to La Gomera')

    rivers_10m = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m')
    land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='face', facecolor=cfeature.COLORS['land'])

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()

    ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax1.set_extent(extent1, crs=ccrs.PlateCarree())
    #ax1.coastlines(resolution='50m')
    ax1.add_feature(land_10m)
    #ax1.add_feature(pop_10m)
    #ax1.add_feature(rivers_10m, facecolor='None', edgecolor='b', alpha=0.5)
    ax1.set_xticks([-20,-15,-10,-5, 0, 5])
    ax1.xaxis.set_major_formatter(lon_formatter)
    ax1.set_yticks([25,30,35,40,45,50])
    ax1.yaxis.set_major_formatter(lat_formatter)
    ax1.plot(lon_exmouth, lat_exmouth, marker='o', color='blue', markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax1.plot(lon_la_gomera, lat_la_gomera, marker='o', color='blue', markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax1.plot(lon_route,lat_route, ':',transform=ccrs.PlateCarree())
    ax1.plot(lon_boat, lat_boat, marker='o', color='red', markersize=8, alpha=0.7, transform=ccrs.PlateCarree())
    ax1.set_title('Expedition chart')

    ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.PlateCarree())
    ax2.add_feature(land_10m)
    ax2.set_xticks([-20,-15,-10,-5, 0, 5])
    ax2.xaxis.set_major_formatter(lon_formatter)
    ax2.set_yticks([25,30,35,40,45,50])
    ax2.yaxis.set_major_formatter(lat_formatter)
    ax2.plot(lon_exmouth, lat_exmouth, marker='o', color='blue', markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax2.plot(lon_la_gomera, lat_la_gomera, marker='o', color='blue', markersize=4, alpha=0.7, transform=ccrs.PlateCarree())
    ax2.plot(lon_route,lat_route, ':',transform=ccrs.PlateCarree())
    ax2.plot(lon_boat, lat_boat, marker='o', color='red', markersize=8, alpha=0.7, transform=ccrs.PlateCarree())
    ax2.set_title('Chart of the day')
    ax2.set_extent(extent2)

    plt.show()
    #plt.savefig("plots/Exmouth_RC_virtual_row_winter_2020--2021.pdf")
    #plt.savefig("plots/Exmouth_RC_virtual_row_winter_2020--2021.png")

        
if __name__ == "__main__":
    main()
