from lxml import etree
import random
import os


def writeGeo(graph, num_nodes, track_dict):
    xMax = num_nodes * 5
    yMax = num_nodes * 5
    # xNode_position = 0
    # yNode_position = 0
    list_x_coords = []
    list_y_coords = []
    for x in range(0, xMax):
        list_x_coords.append(x)
    for y in range(0, yMax):
        list_y_coords.append(y)

    node_coords_dict = {}


    root_Geographic = etree.Element("Layout", version="1.0", xMin="0", yMin="0", xMax=str(xMax), yMax=str(yMax), xmlns="https://www.tracsis.com/infrastructure")
    child1_Geographic = etree.SubElement(root_Geographic, "NodePositions")
    child2_Geographic = etree.SubElement(root_Geographic, "TrackSectionPositions")
    child3_Geographic = etree.SubElement(root_Geographic, "LocationLabels")

    for node in graph:
        x = random.choice(list_x_coords)
        y = random.choice(list_y_coords)
        etree.SubElement(child1_Geographic, "NodePosition", id=str(node), x=str(x), y=str(y))
        node_coords_dict[node] = (x, y)

    Geo_edgeID = 1
    for edge in graph.edges():
        string_edge_ID = "tr_"+ str(Geo_edgeID)
        child4_Geographic = etree.SubElement(child2_Geographic, "TrackSectionPosition", id=str(string_edge_ID))
        node1 = node_coords_dict[edge[0]]
        etree.SubElement(child4_Geographic, "Point", x=str(node1[0]), y=str(node1[1]))
        node2 = node_coords_dict[edge[1]]
        etree.SubElement(child4_Geographic, "Point", x=str(node2[0]), y=str(node2[1]))
        track_dict[string_edge_ID] = edge
        Geo_edgeID = Geo_edgeID + 1

    #need to create the "Layout" directory to save Geographic.xml in to
    if os.path.exists("Layout"):
        et_Geographic = etree.ElementTree(root_Geographic)
        et_Geographic.write("Layout/Geographic-edited.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)
    else:
        os.mkdir("Layout")
        et_Geographic = etree.ElementTree(root_Geographic)
        et_Geographic.write("Layout/Geographic.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)