from lxml import etree
import random
import os
import time



def write_con(graph):
    """Does some stuff

  Args:
    foo (int): The foo to bar
    bar (str): Bar to use on foo
    baz (float): Baz to frobnicate

  Returns:
    float: The frobnicated baz
  """
    root_Connectivity = etree.Element("Connectivity", version="1.0", xmlns="https://www.tracsis.com/infrastructure")
    child1_Connectivity = etree.SubElement(root_Connectivity, "Nodes")
    child2_Connectivity = etree.SubElement(root_Connectivity, "TrackSections")

    #dictionary to store track ids and the nodes they connect
    track_dict = {}
    Con_edgeID = 1
    for edge in graph.edges():
        string_edge_ID = "tr_"+ str(Con_edgeID)
        etree.SubElement(child2_Connectivity, "TrackSection", id=str(string_edge_ID), length="100", startNode=str(edge[0]), endNode=str(edge[1]))
        track_dict[string_edge_ID] = edge
        Con_edgeID = Con_edgeID + 1

    for node in graph:
        if graph.nodes[node]['type'] == "LimitOfNetwork":
            track_name = ""
            edges_array = list(graph.edges(node))
            for key, value in track_dict.items():
                if value == edges_array[0] or value == tuple(reversed(edges_array[0])):
                    track_name = key
            etree.SubElement(child1_Connectivity, graph.nodes[node]['type'], id=str(node), type="Unknown", track=track_name)
        elif graph.nodes[node]['type'] == "DummyNode":
            instr = ""
            outstr = ""
            edges_array = list(graph.edges(node))
            for key, value in track_dict.items():
                if value == edges_array[0] or value == tuple(reversed(edges_array[0])):
                    instr = key
            for key, value in track_dict.items():
                if value == edges_array[1] or value == tuple(reversed(edges_array[1])):
                    outstr = key
            etree.SubElement(child1_Connectivity, graph.nodes[node]['type'], id=str(node), in_=instr, out=outstr)
        elif graph.nodes[node]['type'] == "Switch":
            instr = ""
            outMain = ""
            outBranch = ""
            edges_array = list(graph.edges(node))
            for key, value in track_dict.items():
                if value == edges_array[0] or value == tuple(reversed(edges_array[0])):
                    instr = key
            for key, value in track_dict.items():
                if value == edges_array[1] or value == tuple(reversed(edges_array[1])):
                    outMain = key
            for key, value in track_dict.items():
                if value == edges_array[2] or value == tuple(reversed(edges_array[2])):
                        outBranch = key         
            etree.SubElement(child1_Connectivity, graph.nodes[node]['type'], id=str(node), in_=instr, outMain=outMain, outBranch=outBranch, branchDirection="Right")
        elif graph.nodes[node]['type'] == "FlatCrossing":
            inMain = ""
            outMain = ""
            inCross = ""
            outCross = ""
            edges_array = list(graph.edges(node))
            for key, value in track_dict.items():
                if value == edges_array[0] or value == tuple(reversed(edges_array[0])):
                    inMain = key
            for key, value in track_dict.items():
                if value == edges_array[1] or value == tuple(reversed(edges_array[1])):
                    outMain = key
            for key, value in track_dict.items():
                if value == edges_array[2] or value == tuple(reversed(edges_array[2])):
                    inCross = key
            for key, value in track_dict.items():
                if value == edges_array[3] or value == tuple(reversed(edges_array[3])):
                    outCross = key
            etree.SubElement(child1_Connectivity, graph.nodes[node]['type'], id=str(node), inMain=inMain, outMain=outMain, inCross=inCross, outCross=outCross, direction="RightToLeft")


    et_Connectivity = etree.ElementTree(root_Connectivity)
    if os.path.exists("Connectivity.xml"):
        et_Connectivity.write("Connectivity-edited.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)
    else:
        et_Connectivity.write("Connectivity.xml", encoding='utf-8', xml_declaration=True, pretty_print=True)
    return track_dict