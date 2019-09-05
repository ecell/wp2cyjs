import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

__author__ = 'Kozo Nishida'
__email__ = 'knishida@riken.jp'
__version__ = '0.0.1'
__license__ = 'MIT'

API_BASE = 'https://webservice.wikipathways.org/'

def wp2cyelements(identifier):
    gpml = requests.get(API_BASE + 'getPathway?pwId=' + identifier + '&format=json').content
    soup = BeautifulSoup(json.loads(gpml)['pathway']['gpml'], "xml")
    
    wpnodes = soup.find_all('DataNode')
    wpedges = soup.find_all('Interaction')

    cyelements = {}
    cynodes = []
    cyedges = []

    for wpn in wpnodes:
#        if wpn['Type'] == "Metabolite":
        g = wpn.find('Graphics')
        data = {}
        data['id'] = wpn['GraphId']
        data['label'] = wpn['TextLabel']
        data['x'] = float(g['CenterX'])
        data['y'] = float(g['CenterY'])
        data['width'] = g['Width']
        data['height'] = g['Height']

        cynode = {"data":data, "position":{"x":float(g["CenterX"]), "y":float(g["CenterY"])}, "selected":"false"}
        cynodes.append(cynode)

    for wpe in wpedges:
        data = {}
        for point in wpe.find_all('Point'):
            if point.has_attr('GraphRef') and point.has_attr('ArrowHead'):
                data['target'] = point['GraphRef']
            elif point.has_attr('GraphRef'):
                data['source'] = point['GraphRef']
        cyedge = {"data":data}
        cyedges.append(cyedge)

    cyelements["nodes"] = cynodes
    cyelements["edges"] = cyedges
    return cyelements

def cynodes2df(cynodes):
    rows = []
    for cynode in cynodes:
        rows.append(pd.Series(cynode['data']))
    return pd.DataFrame(rows)

def cyelements2cyjs(cyelements, filename):
    d = {}
    d["elements"] = cyelements
    print(json.dumps(d, indent=4), file=open(filename,'w'))
    print("save cyelements as " + filename)
    
