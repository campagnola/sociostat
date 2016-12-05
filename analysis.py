import numpy as np
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





