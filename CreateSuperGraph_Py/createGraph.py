import networkx as nx
from lxml import etree
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot



def create_graph(path):
    """Create a graph 
  
  Args:
    path (String): Path to folder containing XML documents
  
  Returns:
    Graph: Graph to be used as either a base graph or additional graph
  """
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
    """Display graphs to user for troubleshooting - two graphs
  
  Args:
    graph_A (Graph): Graph structure to be displayed using matplotlib draw
    graph_B (Graph): Graph structure to be displayed using matplotlib draw 


  Returns:
    float: Void
  """
    pos1=nx.spring_layout(graph_A)
    nx.draw(graph_A,pos1, with_labels=True, font_weight='bold')
    plt.show(block=False)
    pos2=nx.spring_layout(graph_B)
    for k,v in pos2.items():
        # Shift the x values of every node by 3 to the right
        v[0] = v[0] +3
    nx.draw(graph_B,pos2, with_labels=True, font_weight='bold')
    plt.show() 

def display_three_graphs(graph_A, graph_B, graph_C):
    """Display graphs to user for troubleshooting - three graphs
  
  Args:
    graph_A (Graph): Graph structure to be displayed using matplotlib draw
    graph_B (Graph): Graph structure to be displayed using matplotlib draw
    graph_C (Graph): Graph structure to be displayed using matplotlib draw


  Returns:
    float: Void
  """
    pos1=nx.spring_layout(graph_A)
    nx.draw(graph_A,pos1, with_labels=True, font_weight='bold')
    plt.show(block=False)
    pos2=nx.spring_layout(graph_B)
    for k,v in pos2.items():
        # Shift the x values of every node by 3 to the right
        v[0] = v[0] +3
    nx.draw(graph_B,pos2, with_labels=True, font_weight='bold')
    plt.show(block=False)
    pos3=nx.spring_layout(graph_C)
    for k,v in pos3.items():
        # Shift the x values of every node by 3 to the right
        v[0] = v[0] +6
    nx.draw(graph_C,pos3, with_labels=True, font_weight='bold')
    plt.show()

def create_graphviz_files(inm, tps, path):
    """Write master data to .dot file for use in GVEdit
  
  Args:
    inm (Graph): Graph structure to be written to file
    tps (Graph): Graph structure to be written to file
    path (String): Path to save the created .dot files

  Returns:
    float: Void
  """
    nx.draw_graphviz(inm)
    nx.write(inm, path + "inm/inm.dot")
    nx.draw_graphviz(tps)
    nx.write(tps, path + "tps/tps.dot")


    
