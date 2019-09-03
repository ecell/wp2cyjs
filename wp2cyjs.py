import json
import requests
from bs4 import BeautifulSoup

import pandas as pd

__author__ = 'Kozo Nishida'
__email__ = 'knishida@riken.jp'
__version__ = '0.0.1'
__license__ = 'MIT'

API_BASE = 'https://webservice.wikipathways.org/'

def wp2cyjs(identifier):
    gpml = requests.get(API_BASE + 'getPathway?pwId=' + identifier + '&format=json').content
    soup = BeautifulSoup(json.loads(gpml)['pathway']['gpml'], "xml")
    
    wpnodes = soup.find_all('DataNode')
    wpedges = soup.find_all('Interaction')

    cyelements = {}
    cynodes = []
    cyedges = []

    for wpn in wpnodes:
        g = wpn.find('Graphics')
        data = {}
        data['id'] = wpn['GraphId']
        data['label'] = wpn['TextLabel']
        data['x'] = float(g['CenterX'])
        data['y'] = float(g['CenterY'])
        data['width'] = g['Width']
        data['height'] = g['Height']

        cynode = {"data":data, "position":{"x":float(g["CenterX"]), "y":float(g["CenterY"])}, "selected":"false"}
        cynodes.append(node)

    for wpe in wpedges:
        data = {}
        data['source'] = wpe.find_all('Point')[0]['GraphRef']
        data['target'] = wpe.find_all('Point')[1]['GraphRef']
        cyedge = {"data":data}
        cyedges.append(cyedge)

    cyelements["nodes"] = cynodes
    cyelements["edges"] = cyedges
    return elements
