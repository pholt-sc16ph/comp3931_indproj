#!/usr/bin/python
import copy
import random


import matplotlib.pyplot as plt
import networkx as nx
from lxml import etree

from graphs import createGraph

while True:
    switch_number = 3
    crossing_number = 3
    # switch_number = input ("Choose number of switch nodes in set one: ")
    # crossing_number = input ("Choose number of crossing nodes in set one: ")
    # number_differences = input ("Choose the number of differences between set one and set two: ")
    break  

G = createGraph(int(switch_number), int(crossing_number))
print(nx.info(G))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

root = etree.Element("Connectivity", version="1.0", xmlns="https://www.tracsis.com/infrastructure")
child1 = etree.SubElement(root, "Nodes")
child2 = etree.SubElement(root, "TrackSections")

for node in G:
    if G.nodes[node]['type'] == "LimitOfNetwork":
        etree.SubElement(child1, G.nodes[node]['type'], id=str(node), type="Unknown", track="4")
    elif G.nodes[node]['type'] == "Switch":
        in_var = "in"
        etree.SubElement(child1, G.nodes[node]['type'], id=str(node), in_="track", outMain="f", outBranch="o", branchDirection="Right")
    elif G.nodes[node]['type'] == "FlatCrossing":
        etree.SubElement(child1, G.nodes[node]['type'], id=str(node), inMain="f", outMain="d", inCross="f", outCross="g", direction="RighttoLeft")

edgeID = 1
for edge in G.edges():
    etree.SubElement(child2, "TrackSection", id=str(edgeID), length="100", startNode=str(edge[0]), endNode=str(edge[1]))
    edgeID = edgeID + 1


print(G.edges())
et = etree.ElementTree(root)
et.write("sample.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)