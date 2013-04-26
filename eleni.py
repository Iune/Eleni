#!/usr/local/bin/python
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("basin", help="Tropical Cyclone Basin")
parser.add_argument("year", help="Year")
parser.add_argument("name", help="Storm Name (Used in File)")
parser.add_argument("--sat", help="NASA Blue Marble Background Image", action="store_true")
parser.add_argument("--scale", help="Tropical Cyclone Intensity Scale")

args = parser.parse_args()

ask_name = args.name
ask_basin = args.basin
ask_year = args.year

data_file_location = "Data/%s/%s/%s-%s.csv" % (ask_basin,ask_year,ask_name,ask_year)
#data_file_location = "Data/EPac/2011/Jova-2011.csv"
rows = []
f = open(data_file_location, 'rb')
reader = csv.reader(f, skipinitialspace = True)
rows = zip(*reader)
f.close()

lat = list(rows[8])
lon = list(rows[9])
winds = list(rows[10])
year = int(rows[1][0])
storm_num = int(rows[2][0])
storm_name = str(rows[5][0])
k = 0
while k < len(lon):
    lon[k] = float(lon[k])
    k = k + 1

k = 0
while k < len(lat):
    lat[k] = float(lat[k])
    k = k + 1

k = 0
while k < len(winds):
    winds[k] = float(winds[k])
    k = k + 1
    
scale_SSHS = ['#c0c0c0', '#5ebaff', '#00faf4', '#ffffcc', '#ffe775', '#ffc140', '#ff8f20', '#ff6060']
scale_JMA = ['#c0c0c0', '#5ebaff', '#00faf4', '#ccffff', '#fdaf9a']
scale_MFR = ['#c0c0c0', '#80ccff', '#5ebaff', '#00faf4', '#ccffff', '#ffffcc', '#ffc140', '#ff6060']
scale_IMD = ['#c0c0c0', '#80ccff', '#5ebaff', '#00faf4', '#ccffff', '#ffc140', '#ff6060']
scale_AUS = ['#c0c0c0', '#5ebaff', '#00faf4', '#ccffff', '#ffffcc', '#ffc140', '#ff6060']

categories = []

if args.scale:
    if args.scale == 'JMA':
        k = 0
        while k < len(winds):
            if winds[k] < 32.5 and winds[k] != 0:
                categories.append(scale_JMA[1])
            elif winds[k] >= 32.5 and winds[k] <52.5:
                categories.append(scale_JMA[2])
            elif winds[k] >= 52.5 and winds[k] <62.5:
                categories.append(scale_JMA[3])
            elif winds[k] >= 62.5:
                categories.append(scale_JMA[4])
            else:
                categories.append(scale_JMA[0])
            k = k + 1
    elif args.scale == 'MFR':
        k = 0
        while k < len(winds):
            if winds[k] < 28 and winds[k] != 0:
                categories.append(scale_MFR[1])
            elif winds[k] >= 28 and winds[k] <34:
                categories.append(scale_MFR[2])
            elif winds[k] >= 34 and winds[k] <48:
                categories.append(scale_MFR[3])
            elif winds[k] >= 48 and winds[k] <64:
                categories.append(scale_MFR[4])
            elif winds[k] >= 64 and winds[k] <90:
                categories.append(scale_MFR[5])
            elif winds[k] >= 90 and winds[k] <115:
                categories.append(scale_MFR[6])
            elif winds[k] >= 115:
                categories.append(scale_MFR[7])
            else:
                categories.append(scale_MFR[0])
            k = k + 1
    elif args.scale == 'AUS':
        k = 0
        while k < len(winds):
            if winds[k] < 34:
                categories.append(scale_AUS[1])
            elif winds[k] >= 34 and winds[k] <48:
                categories.append(scale_AUS[2])
            elif winds[k] >= 48 and winds[k] <64:
                categories.append(scale_AUS[3])
            elif winds[k] >= 64 and winds[k] <90:
                categories.append(scale_AUS[4])
            elif winds[k] >= 90 and winds[k] <115:
                categories.append(scale_AUS[5])
            elif winds[k] >= 115:
                categories.append(scale_AUS[6])
            else:
                categories.append(scale_AUS[0])
            k = k + 1
    elif args.scale == 'IMD':
        k = 0
        while k < len(winds):
            if winds[k] < 28 and winds[k] != 0:
                categories.append(scale_IMD[1])
            elif winds[k] >= 28 and winds[k] <34:
                categories.append(scale_IMD[2])
            elif winds[k] >= 34 and winds[k] <48:
                categories.append(scale_IMD[3])
            elif winds[k] >= 48 and winds[k] <64:
                categories.append(scale_IMD[4])
            elif winds[k] >= 64 and winds[k] <120:
                categories.append(scale_IMD[5])
            elif winds[k] >= 120:
                categories.append(scale_IMD[6])
            else:
                categories.append(scale_IMD[0])
            k = k + 1
else:
    k = 0
    while k < len(winds):
        if winds[k] < 32.5 and winds[k] != 0:
            categories.append(scale_SSHS[1])
        elif winds[k] >= 32.5 and winds[k] <62.5:
            categories.append(scale_SSHS[2])
        elif winds[k] >= 62.5 and winds[k] <82.5:
            categories.append(scale_SSHS[3])
        elif winds[k] >= 82.5 and winds[k] <98.5:
            categories.append(scale_SSHS[4])
        elif winds[k] >= 98.5 and winds[k] <112.5:
            categories.append(scale_SSHS[5])
        elif winds[k] >= 112.5 and winds[k] <137.5:
            categories.append(scale_SSHS[6])
        elif winds[k] >= 137.5:
            categories.append(scale_SSHS[7])
        else:
            categories.append(scale_SSHS[0])
        k = k + 1
bottom_lon = float(min(lon)) - 5
bottom_lat = float(min(lat)) - 5
top_lon = float(max(lon)) + 5
top_lat = float(max(lat)) + 5

track_title =  "%s Storm #%s \"%s\"" % (year, storm_num, ask_name)
print track_title
#print categories
m = Basemap(llcrnrlon=bottom_lon, llcrnrlat=bottom_lat, 
urcrnrlon=top_lon, urcrnrlat=top_lat, resolution='i',projection='merc')

     
x, y = m(lon, lat) # forgot this line
if args.sat:
    m.bluemarble()
    m.plot(x, y, '-', markersize=0, linewidth=0.75, color='#ffffff', markerfacecolor='b')
else:
    m.drawlsmask(land_color='#f1eee8',ocean_color='#b5d0d0',lakes=True)
    m.drawcoastlines()
    m.plot(x, y, '-', markersize=0, linewidth=0.75, color='#000000', markerfacecolor='b')
save_file_name = "Output/%s %s track.png" % (ask_name,year)
plt.title(track_title) 
plt.scatter(x, y, s=40, c=categories)
plt.savefig(save_file_name, bbox_inches=0) 
plt.show()
