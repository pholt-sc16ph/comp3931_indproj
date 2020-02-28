#!/usr/bin/python
from lxml import etree 
import copy

def Connectivity():
    version = "1.0"
    xmlns = "https://www.tracsis.com/infrastructure"

    master_nodes = []
    master_switch = []
    master_limit = []
    master_crossing = []

    for i in range(10):
        master_switch.append("sw_" + str(i))
        master_limit.append("lm_" + str(i))
        master_crossing.append("cr_" + str(i))

    master_nodes.append(master_switch)
    master_nodes.append(master_limit)
    master_nodes.append(master_crossing)

    editable_nodes = copy.deepcopy(master_nodes)
    # print(editable_nodes)

    #create top level "Connectivity"
    root = etree.Element("Connectivity", version=version, xmlns=xmlns)

    #create Nodes and TrackSections children
    nodes = etree.SubElement(root, "Nodes")
    track_sec = etree.SubElement(root, "TrackSections")
    print(editable_nodes[0])
    #add children to Nodes and TrackSections
    for i in range(10): 
        # print(editable_nodes[0][i])
        popped = editable_nodes[0].pop(0)
        etree.SubElement(nodes, "Switch", id=popped, type="Unknown", track=str(i))
        
    # print(editable_nodes[0].pop(0))
    print(editable_nodes[0])
    etree.SubElement(track_sec, "TrackSection")

    #add top line <?xml version="1.0" encoding="utf-8"?>
    root.addprevious(etree.Comment())


    tree = etree.ElementTree(root)
    tree.write("Connectivity.xml", pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return



def Geographic():
    #create top level "Connectivity"
    root = etree.Element("Layout")

    #create Nodes and TrackSections children
    node_pos = etree.SubElement(root, "NodePositions")
    track_sec = etree.SubElement(root, "TrackSectionPositions")
    etree.SubElement(root, "LocationLabels")

    #add children to Nodes and TrackSections
    etree.SubElement(node_pos, "NodePosition")
    track_sec_pos = etree.SubElement(track_sec, "TrackSectionPosition")
    

    #add children to TrackSections
    etree.SubElement(track_sec_pos, "Point")
    etree.SubElement(track_sec_pos, "Point")

    #add top line <?xml version="1.0" encoding="utf-8"?>
    root.addprevious(etree.Comment())


    tree = etree.ElementTree(root)
    tree.write("Geographic.xml", pretty_print=True, xml_declaration=True, encoding='UTF-8')
    return

Connectivity()
Geographic()
