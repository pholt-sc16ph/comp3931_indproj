#!/usr/bin/python
from lxml import etree 
import copy
import networkx as nx
import matplotlib.pyplot as plt
import random
from graphs import createGraph


while True:
    
    switch_number = input ("Choose number of switch nodes: ")
    crossing_number = input ("Choose number of crossing nodes: ")
    break  

G = createGraph(int(switch_number), int(crossing_number))
print(nx.info(G))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()