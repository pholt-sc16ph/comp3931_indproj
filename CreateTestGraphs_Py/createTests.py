#!/usr/bin/python
import copy
import random
import os
import zipfile
import shutil


import matplotlib.pyplot as plt
import networkx as nx
from lxml import etree

from graphOrig import create_graph
from graphEdit import graph_edit, changes_dict
from editXml import replace_in
from writeGeo import write_geo
from writeCon import write_con
from writeInfo import print_info, write_json_file, write_text_file


def main():

    switch_number = 0
    crossing_number = 0
    number_differences = 0

    while True:
        # dummy_number = 10
        # switch_number = 10
        # crossing_number = 10
        # number_differences = 5
        dummy_number = input ("Choose number of dummy nodes in original graph: ")
        switch_number = input ("Choose number of switch nodes in original graph: ")
        crossing_number = input ("Choose number of crossing nodes in original graph: ")
        number_differences = input ("Choose the number of differences between original graph and edited graph: ")
        break  
    
    """While loop to keep the program running and to accept user input so that the test sets can be generated as an when they are needed.
    The program will create one graph randomly using the data supplied which is then used to create the files to be read by TPSDataviewer.
    The graph which is produced is then edited slightly so as to create another set of files which can be read by TPSDataviewer but with a number of 
    differences (requested by the user)
    For example :
    User requests a graph with 3 switches and 3 crossings, this might produce a graph with 3 limit of networks. If the user selects one difference, 
    then one of these limits is changed into a switch or a crossing and the required number of limit of network nodes are added. This then produces a
    set of two graphs which are basically the same with minor differences.
    The data sets can be made complex with many differences which should represent the final data set to be worked on
    """
    """
    Create original graph and write to a new folder in /Data/automated_tests. The new folder will be named to detail the
    graphs it contains. An example folder name would be:
    "/Data/automated_tests/1-dummy_2-switches_2-crossings_1-changes_45633" (number on the end is a random unique ID to allow 
    folders with the same criteria to be created).
    Inside this folder will have two .orb files, one named original.orb and one named edited.orb, and a .txt file named changes.txt
    containing the differences between the two graphs. 
    An example of the text file would look like:

    2 changes:
    node number: 4("LimitOfNetwork") swapped with node number: 4("Switch") - nodes created as a result: 15("LimitOfNetwork") and 16("LimitOfNetwork")
    node number: 7("Switch") deleted - nodes deleted as a result: 9("LimitOfNetwork") and 10("LimitOfNetwork")

    """
    path_to_automated_tests = "../Data/automated_tests/"
    random_file_number = random.randint(100000, 999999)
    directory_string = str(dummy_number) + "-dummy_" + str(switch_number) + "-switch_" + str(crossing_number) + "-crossings_" + str(number_differences) + "-changes_" + str(random_file_number)
    new_directory = path_to_automated_tests + directory_string
    os.makedirs(new_directory)


    # G is the main graph produced, this is different each time create.py is run
    G = create_graph(int(dummy_number),int(switch_number), int(crossing_number))
    number_of_nodes = G.number_of_nodes()
    G.nodes(data=True)
    # use graph created to write Connectivity.xml
    # writeCon() returns a dictionary for use in writeGeo()
    track_dict_original = write_con(G)
    # use graph created to write Geographic.xml and place in Layout folder
    write_geo(G, number_of_nodes, track_dict_original)
    """ to display graphs uncomment the below code """

    #display both graphs for troubleshooting
    # elarge1 =[(u,v) for (u,v,d) in G.edges(data=True)]
    pos1=nx.spring_layout(G)
    nx.draw(G,pos1, with_labels=True, font_weight='bold')
    plt.show(block=False) 
    # plt.draw()

    #call function to replace "in_" with "in" in the Connectivity.xml file
    replace_in()

    zfName = "original_graph.zip"
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

    shutil.move('original_graph.orb', new_directory)



    F = graph_edit(G, int(number_differences))
    number_of_nodes = F.number_of_nodes()
    F.nodes(data=True)
    # use graph created to write Connectivity.xml
    # writeCon() returns a dictionary for use in writeGeo()
    track_dict_edited = write_con(F)
    # use graph created to write Geographic.xml and place in Layout folder
    write_geo(F, number_of_nodes, track_dict_edited)
    """ to display graphs uncomment the below code """

    # elarge2 =[(u,v) for (u,v,d) in F.edges(data=True)]
    pos2=nx.spring_layout(F)
    for k,v in pos2.items():
        # Shift the x values of every node by 3 to the right
        v[0] = v[0] +3
    nx.draw(F,pos2, with_labels=True, font_weight='bold')
    plt.show() # display
    # plt.draw()

    #call function to replace "in_" with "in" in the Connectivity.xml file
    replace_in()


    zfName = "edited_graph.zip"
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

    shutil.move('edited_graph.orb', new_directory)

    # print_info(changes_dict)
    write_json_file(changes_dict, new_directory)
    write_text_file(changes_dict, new_directory)

if __name__ == '__main__':
    main()