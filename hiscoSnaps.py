#!/usr/bin/env python

from rdflib import Graph, URIRef
from rdflib.namespace import SKOS
import csv
import os

dataPath = 'data/'
outputPath = 'output/'

for f in os.listdir(dataPath):
    # Empty SKOS graph for this file
    g = Graph()
    with open(dataPath + f, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            hisco = row[0]
            # Discard row if not a 5-digit HISCO
            if not len(hisco.split('-')[-1]) == 5:
                continue
            # Each row is the URI of a different HISCO in this year
            hiscoURI = URIRef(hisco)
            # Genearate unit, minor, major and root nodes and relations
            unitURI = URIRef(hisco[:-2])
            minorURI = URIRef(hisco[:-3])
            majorURI = URIRef(hisco[:-4])
            rootURI = URIRef(hisco[:-6])
            # Insert SKOS relations
            g.add( (hiscoURI, SKOS.broader, unitURI) )
            g.add( (unitURI, SKOS.broader, minorURI) )
            g.add( (minorURI, SKOS.broader, majorURI) )
            g.add( (majorURI, SKOS.broader, rootURI) )
        g.serialize(outputPath + 'skos-' + f.split('.')[0] + '.nt', format='nt')

