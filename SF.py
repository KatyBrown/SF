import conda
import os
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys

def get_spp_dict():
    sppdict = {'Camel': {'diet': 'H', 'region': ['north_africa'], 'is_land': True, 'ind': 1},
                'Giraffe': {'diet': 'H', 'region': ['south_africa'], 'is_land': True, 'ind': 2},
                'Cow': {'diet': 'H', 'region': ['all'], 'is_land': True, 'ind': 3},
                'Brown_Bear': {'diet': 'C', 'region': ['north_america', 'east_europe', 'north_america'], 'is_land': True, 'ind': 4},
                'Lion': {'diet': 'C', 'region': ['south_africa'], 'is_land': True, 'ind': 5},
                'Tiger': {'diet': 'C', 'region': ['south_asia'], 'is_land': True, 'ind': 6},
                'Killer_Whale': {'diet': 'C', 'region': ['all'], 'is_land': False, 'ind': 7},
                'Dolphin': {'diet': 'C', 'region': ['all'], 'is_land': False, 'ind': 8},
                'Blue_Whale': {'diet': 'C', 'region': ['all'], 'is_land': False, 'ind': 9},
                'Koala': {'diet': 'H', 'region': ['australia'], 'is_land': True, 'ind': 10},
                'Kangaroo': {'diet': 'H', 'region': ['australia'], 'is_land': True, 'ind': 11},
                'Wombat': {'diet': 'H'}, 'region': ['australia'], 'is_land': True, 'ind': 12}
    return(sppdict)

def get_coords():
    coords = {
    'north_africa': ([-20, 50], [0, 35]),
    'south_africa': ([0, 50], [-35, 0]),
    'australia': ([115, 150], [-40, -10]),
    'europe': ([-10, 30], [30, 70]),
    'east_europe': ([10, 30], [40, 70]),
    'north_asia': ([40, 160], [40, 70]),
    'south_asia': ([70, 160], [0, 35]),    
    'south_america': ([-75, -40], [-55, 10]),
    'north_america': ([-155, -60], [10, 70]),
    'pacific_1': ([-180, -80], [-65, 10]),
    'pacific_2': ([-180, -120], [0, 45]),
    'pacific_3': ([120, 180], [-10, 50]),
    'atlantic_1': ([-70, 0,], [0, 60]),
    'atlantic_2': ([-70, 0], [-60, 0])}
    return (coords)

def fix_regions(regions):
    coords = get_coords()
    if 'all' in regions:
        return (list(coords.keys()))
    for region in regions:
        if region not in coords:
            regions.remove(region)
            for c in coords:
                if region in c:
                    regions.append(c)
    return(regions)

def points_in_region(regions, npoints, is_land):
    regions = fix_regions(regions)
    m = Basemap(projection='cyl',llcrnrlat=-65,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    points = []
    coords = get_coords()
    i = 0
    while i < npoints:
        region = regions[np.random.randint(0, len(regions))]
        x_point = np.random.randint(coords[region][0][0], coords[region][0][1])
        y_point = np.random.randint(coords[region][1][0], coords[region][1][1])
        if m.is_land(x_point, y_point) == is_land:
            points.append((x_point, y_point))
            i += 1
    return (points)


def plot_map(regions, npoints, colour='red', is_land=True):
    plt.figure(figsize=(20, 20))
    m = Basemap(projection='cyl',llcrnrlat=-65,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    m.fillcontinents(color='#e5d381',
                     lake_color='#b4dbf3')
    m.drawmapboundary(fill_color='#b4dbf3')
    points = points_in_region(regions, npoints, is_land)
    for p in points:
        m.scatter(p[0], p[1], latlon=True, zorder=100, color=colour)
    return (m)

def getMeans(diet):
    if diet == 'C':
        D = {'Actinobacteria': 0.2534600242717977,
             'Betaproteobacteria': 0.088074848358879784,
             'Chloroflexi': 0.0,
             'Deltaproteobacteria': 0.0,
             'Fusobacteria': 0.40329009511697583,
             'Gammaproteobacteria': 0.2407100610852024,
             'Spirochaetes': 0.010716799730381175,
             'Verrucomicrobia': 0.0037481714367630235}
    elif diet == 'H':
        D = {'Actinobacteria': 0.067299408725901136,
             'Betaproteobacteria': 0.14158572847589096,
             'Chloroflexi': 0.18114644672650754,
             'Deltaproteobacteria': 0.18114644672650754,
             'Fusobacteria': 0.0,
             'Gammaproteobacteria': 0.073026329756470013,
             'Spirochaetes': 0.17633276492538355,
             'Verrucomicrobia': 0.17946287466333927}
    return (D)

def getBacs():
    return (['Fusobacteria', 'Gammaproteobacteria', 'Actinobacteria',
            'Spirochaetes', 'Deltaproteobacteria', 'Betaproteobacteria',
            'Verrucomicrobia', 'Chloroflexi' ])

def generateDataDist(diet, nreads, flux=0.1):
    means = getMeans(diet)
    rmeans = []
    bacs = getBacs()
    for b in bacs:
        m = means[b]
        m2 = np.random.choice(np.arange(max(m-flux, 0), m+flux, 0.01), 1)
        rmeans.append(m2)
    rmeans = [float(r/sum(rmeans)) for r in list(rmeans)]
    nums = np.random.choice(bacs, size=nreads, p=rmeans)
    return (nums)