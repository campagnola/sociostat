import numpy as np
import scipy.stats
import pyqtgraph as pg
import csv

pg.mkQApp()



# Read incident reports
incidents_file = "../SupplementaryMaterials/Data/U.S. Police Shootings Data (Cleaned).csv"

lines = list(csv.reader(open(incidents_file, 'r'), delimiter=','))
header = lines[0]
lines = lines[1:]

numfields = ["Victim's Age", "Shots Fired", "Was the Shooting Justified?", "Results Page"]

dtype = []
for field in header:
    typ = float if field in numfields else object
    dtype.append((field, typ))

incidents_data = np.empty(len(lines), dtype=dtype)
for i,line in enumerate(lines):
    incidents_data[i] = tuple([np.nan if (dtype[j][1] is float and x == '') else x for j,x in enumerate(line)])

#spw = pg.ScatterPlotWidget()
#spw.setFields([(name, {}) for name in header])
    
#spw.setData(data)
#spw.show()



# Read county-level statistics
map_file = '../SupplementaryMaterials/Data/MapFileData-WithCountyResultsAndCovariates.csv'


lines = list(csv.reader(open(map_file, 'r'), delimiter=','))
header = lines[0]
lines = lines[1:]

dtype = []
for i,field in enumerate(header):
    for line in lines:
        val = line[i]
        if val != 'NA':
            break
    try:
        float(val)
        typ = float
    except:
        typ = object
    if field in ('ID', 'State'):
        field = '%s%d' % (field, i)
    dtype.append((field, typ))

map_data = np.empty(len(lines), dtype=dtype)
for i,line in enumerate(lines):
    map_data[i] = tuple([np.nan if (dtype[j][1] is float and x in ('NA' or '')) else x for j,x in enumerate(line)])


b_w_pop = map_data['BAC_TOT'] / map_data['WA_TOT']


black_shot = map_data['BlackArmed'] + map_data['BlackUnarmed']
white_shot = map_data['WhiteArmed'] + map_data['WhiteUnarmed']

b_w_shot = black_shot / white_shot

#pg.plot(white_shot, black_shot, pen=None, symbol='o')



b_w_assault = (map_data['AssaultsBlack.sum'] / map_data['BAC_TOT']) / (map_data['AssaultsWhite.sum'] / map_data['WA_TOT'])


mask = np.isfinite(b_w_shot) & np.isfinite(b_w_assault)

x = b_w_assault[mask]
y = b_w_shot[mask] / b_w_pop[mask]

lx = np.log(x)
ly = np.log(y)
mask2 = np.isfinite(lx) & np.isfinite(ly)
r,p = scipy.stats.pearsonr(lx[mask2], ly[mask2])

plt = pg.plot(x, y, pen=None, symbol='o', symbolSize=(black_shot + white_shot)[mask] + 5, 
              title="black:white assault vs killing (r=%0.2f p=%0.2f)" % (r, p),
              labels={'left': 'black:white shot normalized by population', 
                      'bottom': 'black:white assaults normalized by population'})



