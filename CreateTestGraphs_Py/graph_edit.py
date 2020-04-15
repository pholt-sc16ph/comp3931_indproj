import networkx as nx
import matplotlib.pyplot as plt
import random


from graph_orig import createGraph


mainGraph = createGraph(3, 3)

def graph_orig(graph):
    G = graph
    print("Data and graph for G")
    G.nodes(data=True)
    print(nx.info(G)) 
    print("\n")
    return G

def graph_edit(graph, no_of_changes):
    F = graph
    
    list_of_nodes = list(F.nodes())    
    for x in range(0, no_of_changes):
        random_node = random.choice(list_of_nodes)
        random_node_degree = F.degree(random_node)
        list_of_nodes.remove(random_node)
        number_of_nodes = F.number_of_nodes()
        random_node_neighbors = list(F.neighbors(random_node))
        random_choice_list = [1, 2, 5]
        random_action = random.choice(random_choice_list)
        print("Random action: " + str(random_action))
        print("Node to be acted upon: " + str(random_node))
        #if 1 swap with limit node
        if random_action == 1:
            F.remove_node(random_node)
            lost_nodes = []
            for node in F:
                    if F.degree(node) == 0:
                        lost_nodes.append(node)
            if len(lost_nodes) > 0:
                    for item in lost_nodes:
                        F.remove_node(item)
                        random_node_neighbors.remove(item)
            F.add_node(random_node)
            F.add_edge(random_node, random.choice(random_node_neighbors))
        #if 2 add in a dummy node between two nodes
        if random_action == 2:
            choose_random_neighbour = random.choice(random_node_neighbors)
            F.remove_edge(random_node, choose_random_neighbour)
            new_node = number_of_nodes
            F.add_node(new_node)
            F.add_edge(new_node, random_node)
            F.add_edge(new_node, choose_random_neighbour)
        #if 3 swap with dummy node

        #if 4 swap with switch node

        #if 5 swap with crossing node

        #if 6 just remove node
        if random_action == 6:
            F.remove_node(random_node)
            random_choice_list_6 = [0, 1]
            random_choice_6 = random.choice(random_choice_list_6)
            #when deleting a node there might be nodes which were limitofnetworks which are now floating lost
            #need to decide whether to delete these nodes or connect them to the other nodes which were connected to 
            #the deleted node
            lost_nodes = []
            for node in F:
                    if F.degree(node) == 0:
                        lost_nodes.append(node)
            if random_choice_6 == 0:
                if len(lost_nodes) > 0:
                    for item in lost_nodes:
                        F.remove_node(item)
            if random_choice_6 == 1:
                if len(lost_nodes) == 1:
                    F.add_edge(lost_nodes[0], random_node_neighbors[0])
                    F.add_edge(lost_nodes[0], random_node_neighbors[1])
                elif len(lost_nodes) == 2:
                    F.add_edge(lost_nodes[0], random_node_neighbors[0])
                    F.add_edge(lost_nodes[0], random_node_neighbors[1])
                    F.add_edge(lost_nodes[1], random_node_neighbors[0])
                    F.add_edge(lost_nodes[1], random_node_neighbors[1])

        # 
        # limit_neighbour = list(F.neighbors(random_limit))
        # F.remove_node(random_limit)
        # F.add_node(random_limit)
        # F.add_edge(random_limit, limit_neighbour[0])
        # F.add_node(number_of_nodes+1)
        # F.add_edge(random_limit, number_of_nodes+1)
        # F.add_node(number_of_nodes+2)
        # F.add_edge(random_limit, number_of_nodes+2)

    # print(random_limit)
    print("Data and graph for F")
    F.nodes(data=True)
    print(nx.info(F))
    print("\n")

    return F

#display both graphs for troubleshooting
G1 = graph_orig(mainGraph)
elarge1 =[(u,v) for (u,v,d) in G1.edges(data=True)]
pos1=nx.spring_layout(G1)
nx.draw(G1,pos1, with_labels=True, font_weight='bold')
plt.show(block=False) 
plt.draw()

G2 = graph_edit(mainGraph, 1)
elarge2 =[(u,v) for (u,v,d) in G2.edges(data=True)]
pos2=nx.spring_layout(G2)
for k,v in pos2.items():
    # Shift the x values of every node by 3 to the right
    v[0] = v[0] +3
nx.draw(G2,pos2, with_labels=True, font_weight='bold')
plt.show() # display
plt.draw()