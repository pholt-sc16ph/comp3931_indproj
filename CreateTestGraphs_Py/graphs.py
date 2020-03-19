#create a graph from user input, user will decide the number of nodes and edges

import networkx as nx
import matplotlib.pyplot as plt
import random


def createGraph( switch, crossing):
    G = nx.Graph()
    switch_counter = switch
    crossing_counter = crossing
    G.add_node(0, type="limit")
    node_list = [0]
    node_number = 1
    for counter in range(switch_counter+crossing_counter):
        
        random_type = random.choice([0,1])
        if switch_counter == 0:
            G.add_node(node_number, type="crossing")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            crossing_counter -= 1
            node_list.append(node_number)
        elif crossing_counter == 0:
            G.add_node(node_number, type="switch")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            switch_counter -= 1
            node_list.append(node_number)
        elif random_type == 0 and switch_counter > 0:
            G.add_node(node_number, type="switch")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            switch_counter -= 1
            node_list.append(node_number)
        elif random_type == 1 and crossing_counter > 0:
            G.add_node(node_number, type="crossing")
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            G.add_edge(random.choice(node_list), node_number)
            if 0 in node_list:
                node_list.remove(0)
            crossing_counter -= 1
            node_list.append(node_number)
        for node in G:
            if G.nodes[node]['type'] == 'switch' and G.degree[node] == 3:
                if node in node_list:
                    node_list.remove(node)
            elif G.nodes[node]['type'] == 'crossing' and G.degree[node] == 4:
                if node in node_list:
                    node_list.remove(node)
        node_number += 1

    add_limit_node_number = len(G.nodes())
    for node in node_list:
        node
        if G.nodes[node]['type'] == 'switch' and G.degree[node] == 1:
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'switch' and G.degree[node] == 2:
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'crossing' and G.degree[node] == 1:
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'crossing' and G.degree[node] == 2:
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif G.nodes[node]['type'] == 'crossing' and G.degree[node] == 3:
            G.add_node(add_limit_node_number, type="limit")
            G.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
    return G
    










#    
    


