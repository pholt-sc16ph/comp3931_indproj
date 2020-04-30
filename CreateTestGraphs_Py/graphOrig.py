#create a graph from user input, user will decide the number of nodes and edges

import networkx as nx
import matplotlib.pyplot as plt
import random


def create_graph(dummy, switch, crossing):
    """Does some stuff

  Args:
    foo (int): The foo to bar
    bar (str): Bar to use on foo
    baz (float): Baz to frobnicate

  Returns:
    float: The frobnicated baz
  """
    G = nx.Graph()
    dummy_counter = dummy
    switch_counter = switch
    crossing_counter = crossing

    G.add_node(0, type="LimitOfNetwork")
    node_list = [0]
    node_number = 1
    # print("Adding base nodes")
    for counter in range(dummy_counter+switch_counter+crossing_counter):
        choice_list = ["dummy", "switch", "crossing"]        
        if dummy_counter == 0:
            choice_list.remove("dummy")
        if switch_counter == 0:
            choice_list.remove("switch")
        if crossing_counter == 0:
            choice_list.remove("crossing")
        if choice_list:
            random_type = random.choice(choice_list)
        if crossing_counter == 0 and switch_counter == 0 and dummy_counter == 0:
            #do nothing
            dummy = 0
        elif crossing_counter == 0 and switch_counter == 0:
            # print("if crossing_counter == 0 and switch_counter == 0")
            G.add_node(node_number, type="DummyNode")
            # edge_choice = random.choice(node_list)
            # G.add_edge(edge_choice, node_number)
            # node_list.remove(edge_choice)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            dummy_counter -= 1
            node_list.append(node_number)
        elif switch_counter == 0 and dummy_counter == 0:
            # print("switch_counter == 0 and dummy_counter == 0")
            G.add_node(node_number, type="FlatCrossing")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            crossing_counter -= 1
            node_list.append(node_number)
        elif crossing_counter == 0 and dummy_counter == 0:
            # print("crossing_counter == 0 and dummy_counter == 0")
            G.add_node(node_number, type="Switch")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            switch_counter -= 1
            node_list.append(node_number)
        elif random_type == "dummy" and dummy_counter > 0:
            # print("random_type == 'dummy' and dummy_counter > 0")
            G.add_node(node_number, type="DummyNode")
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            dummy_counter -= 1
            node_list.append(node_number)
        elif random_type == "switch" and switch_counter > 0:
            # print("random_type == 'switch' and switch_counter > 0")
            G.add_node(node_number, type="Switch")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                G.add_edge(0, node_number)
                node_list.remove(0)
            switch_counter -= 1
            node_list.append(node_number)
        elif random_type == "crossing" and crossing_counter > 0:
            # print("random_type == 'crossing' and crossing_counter > 0")
            G.add_node(node_number, type="FlatCrossing")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            crossing_counter -= 1
            node_list.append(node_number)
        
        node_number += 1

    
        # print("Remove nodes which satisfy type and degree")
        for node in G:
            if G.nodes[node]['type'] == 'Switch' and G.degree[node] == 3:
                # print("Remove: G.nodes[node]['type'] == 'Switch' and G.degree[node] == 3")
                if node in node_list:
                    node_list.remove(node)
            elif G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 4:
                # print("Remove: G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 4")
                if node in node_list:
                    node_list.remove(node)
            elif G.nodes[node]['type'] == 'DummyNode' and G.degree[node] == 2:
                # print("Remove: G.nodes[node]['type'] == 'DummyNode' and G.degree[node] == 2")
                if node in node_list:
                    node_list.remove(node)
    

    add_limit_node_number = len(G.nodes())
    # print("Adding LimitOFNetwork to nodes whcih dont have the correct degree for their type")
    for node in node_list:
        node
        if G.nodes[node]['type'] == 'DummyNode' and G.degree[node] == 1:
            # print("G.nodes[node]['type'] == 'DummyNode' and G.degree[node] == 1")
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'Switch' and G.degree[node] == 1:
            # print("G.nodes[node]['type'] == 'Switch' and G.degree[node] == 1")
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'Switch' and G.degree[node] == 2:
            # print("G.nodes[node]['type'] == 'Switch' and G.degree[node] == 2")
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 1:
            # print("G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 1")
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 2:
            # print("G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 2")
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 3:
            # print("G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 3")
            G.add_node(add_limit_node_number, type="LimitOfNetwork")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
    """Graph data for originally made graph"""
    """
    print("Data and graph for G")
    print(type(nx.number_connected_components(G)))
    print(nx.info(G)) 
    print("\n")
    """
    return G