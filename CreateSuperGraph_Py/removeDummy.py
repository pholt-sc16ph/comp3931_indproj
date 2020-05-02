

#can only call on one graph at a time as can only return one graph at a time. Possible to return an array of graphs
def remove_dummy(graph):
    G = graph

    list_of_dummy_nodes = []
    dummy_nodes_with_no_dummy_neighbours = [] #can safely remove and just join up its neighbours
    dummy_nodes_with_one_dummy_neighbour = [] #end dummys in a sequence of dummys
    dummy_nodes_with_two_dummy_neighbours = [] #middle dummys in a sequence of dummys
    list_of_dummy_chains = [] #2d array of chains
    master_list_dummy_chains = []
    edges_to_add_single = []
    edges_to_add_chain = []

    #get master list of all dummy nods to be removed
    for node in G:
        if G.degree[node] == 2:
            list_of_dummy_nodes.append(node)

    #get type of dummy node from master list
        #if dummy node as no dummy node neighbours, safe to delete and add edge between neighbours
        #if dummy node has one dummy neighbour, it must be at the end of a chain, but still in a chain
        #if dummy node as two dummy neighbours it must be in a chain of three or more dummy nodes
    for node in list_of_dummy_nodes:
        neighbours = list(G[node])
        if G.degree(neighbours[0]) != 2 and G.degree(neighbours[1]) == 2:
            dummy_nodes_with_one_dummy_neighbour.append(node)
        elif G.degree(neighbours[0]) == 2 and G.degree(neighbours[1]) != 2:
            dummy_nodes_with_one_dummy_neighbour.append(node)
        elif G.degree(neighbours[0]) != 2 and G.degree(neighbours[1]) != 2:
            dummy_nodes_with_no_dummy_neighbours.append(node)
        else:
            dummy_nodes_with_two_dummy_neighbours.append(node)
    
    #create lists of all the chains possible in graph. this creates duplicates and sub chains of chains
    for dummy in list_of_dummy_nodes:
        neighbours = list(G[dummy])
        chain = [dummy]
        for dummy2 in list_of_dummy_nodes:
            neighbours2 = list(G[dummy2])
            if neighbours2[0] in chain:
                chain.append(dummy2)
            if neighbours2[1] in chain:
                chain.append(dummy2)
        list_of_dummy_chains.append(chain)
    
    #remove safe dummy nodes
    for item in list_of_dummy_chains[:]:
        if len(item) == 1:
            list_of_dummy_chains.remove(item)

    #remove subchains and equivalent chains
    for item in list_of_dummy_chains[:]:
        for item2 in list_of_dummy_chains[:]:
            if item == item2:
                master_list_dummy_chains.append(item)
            else:
                for entry in item:
                    for entry2 in item2:
                        if entry in item2:
                            if item2 in list_of_dummy_chains:
                                list_of_dummy_chains.remove(item2)

    for chain in master_list_dummy_chains:
        edge_tuple = ()
        neighbour_one = ""
        neighbour_two = ""
        for node in chain:
            neighbours = list(G[node])
            if neighbours[0] not in chain:
                neighbour_one = neighbours[0]
            if neighbours[1] not in chain:
                neighbour_two = neighbours[1]
        edge_tuple = edge_tuple + (neighbour_one, neighbour_two)
        edges_to_add_chain.append(edge_tuple)
    
    for node in dummy_nodes_with_no_dummy_neighbours:
        neighbours = list(G[node])
        edge_tuple = (neighbours[0], neighbours[1])
        edge_tuple2 = (neighbours[1], neighbours[0])
        edges_to_add_single.append(edge_tuple)


    for node in list_of_dummy_nodes:
        G.remove_node(node)
    G.add_edges_from(edges_to_add_single)
    G.add_edges_from(edges_to_add_chain)
    return G
