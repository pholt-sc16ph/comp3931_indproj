#!/usr/bin/python
import copy
import random
import os
import zipfile


import matplotlib.pyplot as plt
import networkx as nx
from lxml import etree

from graph_orig import createGraph
from editxml import replace_in
from writeGeo import writeGeo
from writeCon import writeCon



"""
While loop to keep the program running and to accept user input so that the test sets can be generated as an when they are needed.
The program will create one graph randomly using the data supplied which is then used to create the files to be read by TPSDataviewer.
The graph which is produced is then edited slightly so as to create another set of files which can be read by TPSDataviewer but with a number of 
differences (requested by the user)
For example :
User requests a graph with 3 switches and 3 crossings, this might produce a graph with 3 limit of networks. If the user selects one difference, 
then one of these limits is changed into a switch or a crossing and the required number of limit of network nodes are added. This then produces a
set of two graphs which are basically the same with minor differences.
The data sets can be made complex with many differences which should represent the final data set to be worked on
"""
switch_number = 0
crossing_number = 0
number_differences = 0

while True:
    switch_number = 3
    crossing_number = 3
    # switch_number = input ("Choose number of switch nodes in set one: ")
    # crossing_number = input ("Choose number of crossing nodes in set one: ")
    # number_differences = input ("Choose the number of differences between set one and set two: ")
    break  


# G is the main graph produced, this is different each time create.py is run
G = createGraph(int(switch_number), int(crossing_number))
number_of_nodes = G.number_of_nodes()
G.nodes(data=True)
print(nx.info(G))




# use graph created to write Connectivity.xml
# writeCon() returns a dictionary for use in writeGeo()
track_dict = writeCon(G)
# use graph created to write Geographic.xml and place in Layout folder
writeGeo(G, number_of_nodes, track_dict)


"""display G using matplotlib (this won't be the same visually as the graph dsiplayed in TPSDataviewer)"""
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()

"""call function to replace "in_" with "in" in the Connectivity.xml file"""
replace_in()

random_file_number = random.randint(10000, 99999)
dynamic_file_name = "s-" + str(switch_number) + "c-" + str(crossing_number) + "_id-" + str(random_file_number)

zfName = dynamic_file_name + ".zip"
foo = zipfile.ZipFile(zfName, 'w')
foo.write("Connectivity.xml")
# Adding files from directory 'files'
for root, dirs, files in os.walk('Layout'):
    for f in files:
        foo.write(os.path.join(root, f))
foo.close()


pre, ext = os.path.splitext(zfName)
os.rename(zfName, pre + ".orb")

os.remove("Connectivity.xml")
os.remove("Layout/Geographic.xml")
os.removedirs("Layout")