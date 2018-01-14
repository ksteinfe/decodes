import decodes.core as dc
from decodes.core import *

# number of lines in the header
# holds true for ALL EPW files
number_of_epw_header_lines = 8
# a dictionary that maps keystrings to column positions
# not a comprehensive list. for a complete listing, see
# apps1.eere.energy.gov/buildings/energyplus/
#         pdfs/weatherdatainformation.pdf
epw_keycols = {
    "DirNormIrad": 14, #direct normal irradiance (w/m2)
    "DifHorzIrad": 15, #diffuse horizontal irradiance (w/m2)
    "OpqSkyCvr": 23 , #opaque sky cover (tenths of sky)
    "DryBulbTemp": 6 , #dry bulb temperature (deg C)
    "DewPtTemp": 7 , #dew point temperature (deg C)
    "RelHumid": 8 , #relative humidity (%)
    "Pressure": 9 , #atmospheric station pressure (Pa)
    "WindDir": 20 , #wind direction (degrees)
    "WindSpd": 21 , #wind speed (m/s)
    "PreciptWater": 28 , #precipitable water (mm)
    "AeroDepth": 29 , #aerosol depth (1000ths)
    "SnowDepth": 30 , #snow depth (cm)
    "YearOfSample": 0 , #year of sample data
}

def epw_metadata(path):
    """ returns the metadata of an EPW file
    path (string) filepath to the EPW file
    out: a dict containing EPW metadata
    """
    with open(path) as myfile:
        head=[next(myfile) for x in range(number_of_epw_header_lines)]
    
    #city,state/province/region,country,data source,wmo number,lat,long,timezone,elevation
    #LOCATION,San Francisco Intl Ap,CA,USA,TMY3,724940,37.62,-122.40,-8.0,2.0
    dict = {}
    vals = head[0].split(",")
    dict['name'] = vals[1]
    dict['state'] = vals[2]
    dict['country'] = vals[3]
    dict['datasource'] = vals[4]
    dict['wmo'] = int(vals[5])
    dict['lat'] = float(vals[6])
    dict['long'] = float(vals[7])
    dict['timezone'] = float(vals[8])
    dict['elevation'] = float(vals[9])
    return dict

def parse_epw_file(path, desired_keys):
    """ parses an EPW file and returns structured data
    path (string) filepath to the EPW file
    desired_keys ([string]) keys indicating the values to be returned.    only keys listed in epw_keycols may be used.    
    out: if desired_keys is a single string, an array of floats is returned, if desired_keys is an array of keys, an array of dicts is returned.
    """
    skip = number_of_epw_header_lines
    file = open(path) # open the file
    lineno = 0 # keeps track of how many lines have been parsed
    hours = [] #initalize an empty list where we'll store our dicts
    for line in file:
        if lineno >= skip : # only parse this line if past the header
            hourdict = _parse_epw_line(line, desired_keys) # parse line
            if hourdict is not None : 
                hours.append(hourdict)
        lineno += 1 # keep track of how many lines have been parsed
        if lineno > 8760+skip : break
    return hours

def _parse_epw_line(string, desired_keys):
    vals = string.split(",")
    if isinstance(desired_keys, str):
        return float(vals[epw_keycols[desired_keys]])
    else : 
        return {k:float(vals[epw_keycols[k]]) for k in desired_keys}
