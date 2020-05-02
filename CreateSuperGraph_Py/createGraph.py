import networkx as nx
from lxml import etree
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot



def create_graph(path):
    
    G = nx.MultiGraph()
    tree = etree.parse(path)
    root = tree.getroot()
    
    for node in root[0]:
        parts = node.tag.split("}")
        node_type = parts[1]
        node_id = node.get("id")
        G.add_node(node_id, type=node_type)
    for edge in root[1]:
        edge_start = edge.get("startNode")
        edge_end = edge.get("endNode")
        G.add_edge(edge_start, edge_end)
    
    return G


def display_graphs(graph_A, graph_B):
    
    pos1=nx.spring_layout(graph_A)
    nx.draw(graph_A,pos1, with_labels=True, font_weight='bold')
    plt.show(block=False)
    pos2=nx.spring_layout(graph_B)
    for k,v in pos2.items():
        # Shift the x values of every node by 3 to the right
        v[0] = v[0] +3
    nx.draw(graph_B,pos2, with_labels=True, font_weight='bold')
    plt.show() 

def create_graphviz_files(inm, tps, path):
    nx.draw_graphviz(inm)
    nx.write(inm, path + "inm/inm.dot")
    nx.draw_graphviz(tps)
    nx.write(tps, path + "tps/tps.dot")


    
