import networkx as nx
import json
import enum


# Using enum class create enumerations for comparing values of Node names
class nodeValues(enum.Enum):
   LimitOfNetwork = 1
   DummyNode = 2
   Switch = 3
   FlatCrossing = 4

# Find differences algorithm. Start with a base graph assuming the base graph is correct. Loop through the nodes and create a dictionary of connections. Do the same for second graph
# Algorithm compares dictionaries.
# Start at two nodes which are known to be the same one. In the test graphs this is always assumed to be node zero. For any tracsis based graphs a visual check of the graph needs to be
# made to identify two points(nodes) which are equivalent from which to start from. These nodes need to be the same type i.e. they have the same amount of neighbours.

# The algorithm checks the neighbours of the current nodes and assigns equivalence between two nodes which have the same type
# This example would give equivalence between node 1 in graph A and node 1 in graph B
# Graph A node: 0 || Graph B node: 0
# Graph A node 0 neighbours (without previous node, the one we are currently on): [('1', 'Switch')] length: 1
# Graph B node 0 neighbours (without previous node, the one we are currently on): [('1', 'Switch')] length: 1
# Nodes which need changing: []

# The algorithm takes in to account whether two nodes have two edges between them
# Graph A node: 1 || Graph B node: 1
# Graph A node 1 neighbours (without previous node): [('3', 'Switch'), ('3', 'Switch')] length: 2
# Graph B node 1 neighbours (without previous node): [('3', 'Switch'), ('3', 'Switch')] length: 2
# Nodes which need changing: []

# The algorithm flags when a match can't me made, this happens when there is a difference in the graph. In this case node 65 in graph A is a LimitOfNetwork but the equivalent
# node in graph B is a FlatCrossing. The nodes in question are marked as needing to be changed along with the nodes currently the focus (52 and 52 in this case)
# This information is needed to update the base graph with new nodes along with updating the neighbour information of the parent nodes and also adding in any new nodes created.
# Example 1
# Graph A node: 52 || Graph B node: 52
# Graph A node 52 neighbours (without previous node): [('53', 'FlatCrossing'), ('58', 'FlatCrossing'), ('65', 'LimitOfNetwork')] length: 3
# Graph B node 52 neighbours (without previous node): [('53', 'FlatCrossing'), ('58', 'FlatCrossing'), ('65', 'FlatCrossing')] length: 3
# Nodes which need changing: [(('65', 'LimitOfNetwork'), ('65', 'FlatCrossing'), '52', '52')]
# Example 2
# Graph A node: 5 || Graph B node: 5
# Graph A node 5 neighbours (without previous node): [('7', 'Switch'), ('9', 'FlatCrossing')] length: 2
# Graph B node 5 neighbours (without previous node): [('7', 'Switch'), ('6', 'Switch')] length: 2
# Nodes which need changing: [(('9', 'FlatCrossing'), ('6', 'Switch'), '5', '5')]

# When the algorithm flags up a pair of nodes (or in some cases more than one pair) a decision has to be made about what to do with it. As we are assuming that both graphs
# are correct from their point of view anything which is going to add extra nodes and information to the base graph need to be added. In the example above, Graph A is expecting 
# a LimitOfNetwork node but in Graph B the equivalent node is a FlatCrossing.
# Using enums, values were assigned to each node type and two checks are completed:
# if node in graph B is larger than node in Graph A:
#   Change data in Graph A to match data from Graph B and add necessary nodes

# In example 1, as a FlatCrossing has a higher value than LimitOfNetwork, data from Graph B must be added to Graph A (as it is then assumed this data is missing from Graph A). There
# are four steps which need to be completed for this to happen. Change the type of the node in Graph A ("65") to the type in Graph B, add the neighbours of the node in Graph B to
# the neighbour information of Graph A("65"), add the same neighbours to the actual graph as nodes of their own, and finally update the parent node neighbour information. In
# this case node("52") thinks its neighbours are (FlatCrossing, FlatCrossing, LimitOfNetwork) when its neighbours are now three FlatCrossings

# if node in graph B is smaller than node in Graph A:
#   This could mean one of two things. The smaller node is the same node but Graph B is missing information which is in graph A in which case no change is needed as the information
#   is already in Graph A
#   Or, this smaller node is a completely new node in the graph, this can be checked by looking forward in the graph to see if any of its neighbours are the node we were expecting. If
#   that node is found, "smaller" node is added to graph A along with it's neighbours. If this new node is a large branch then the branch information would be added on each loop.

# In eample 2, Graph A was expecting a FlatCrossing but the node in Graph B was a Switch, by checking the neigbours of the Switch from Graph B, the algorithm identifies that one of its
# neighbours is a FlatCrossing and decided that the Switch is a new node. This needs to be added to Graph A by updating the neighbours of nodes "5" and "9" to include the new node and remove
# each other as neighbours. The new node (and its neighbours) need to then be added to Graph A.


def find_diff(base, additional, start_node_base, start_node_add):
    """Graph matching algorithm - checks both graphs and calculates equality between nodes to return a super graph comprising nodes from both supplied graphs
  Args:
    base (Graph): Graph to be the base graph, nodes from additional graph added to this one
    additional (Graph): Graph to be the additional graph
    start_node_base (String): Node id for start position of base graph
    start_node_add (String): Node id for start position of additional graph
    

  Returns:
    Graph: Super graph which is the result of matching
  """
    G = base
    F = additional
    S = nx.MultiGraph()
    sG = start_node_base
    sF = start_node_add

    G_dict = {}
    F_dict = {}
    

    for node in G:
        neighbours = []
        for item in G.edges(node):
            empty_tuple = ()
            empty_tuple = empty_tuple + (item[1], G.nodes[item[1]]['type'])
            neighbours.append(empty_tuple)
        node_type = G.nodes[node]['type']
        G_dict[node] = {"type": node_type, "neighbours": neighbours}
    
    for node in F:
        neighbours = []
        for item in F.edges(node):
            empty_tuple = ()
            empty_tuple = empty_tuple + (item[1], F.nodes[item[1]]['type'])
            neighbours.append(empty_tuple)
        node_type = F.nodes[node]['type']
        F_dict[node] = {"type": node_type, "neighbours": neighbours}

    eqiv_nodes = [(sG, sF)]
    nodes_need_changing = []
    eqiv_nodes_visted = []
    eqiv_nodes_visted_A = []
    eqiv_nodes_visted_B = []
    #The check for equivalence is done by looking at the currently focused nodes and comparing their neighbours. The decisions on whether
    #a node pair are equivalent needs to be done before the loop can move on to that pair. If they are evivalent then the sizes of their 
    #neighbour list is the same
    for en in eqiv_nodes:
        node_a = en[0]
        node_b = en[1]
        eqiv_nodes_visted.append((node_a, node_b))
        eqiv_nodes_visted_A.append(node_a)
        eqiv_nodes_visted_B.append(node_b)
        node_a_neighbours = G_dict[node_a]['neighbours']
        node_a_neighbours_no_previous = []
        for item in node_a_neighbours:
            if item[0] not in eqiv_nodes_visted_A:
                node_a_neighbours_no_previous.append(item)
        node_b_neighbours = F_dict[node_b]['neighbours']
        node_b_neighbours_no_previous = []
        for item in node_b_neighbours:
            if item[0] not in eqiv_nodes_visted_B:
                node_b_neighbours_no_previous.append(item)

        len_a_neigh = len(node_a_neighbours_no_previous)
        len_b_neigh = len(node_b_neighbours_no_previous)
        
        #If neighbour list is of length 1 
        if len_a_neigh == 1 and  len_b_neigh == 1:
            for node_A in node_a_neighbours_no_previous[:]:
                for node_B in node_b_neighbours_no_previous[:]:
                    if node_A[1] == node_B[1]:
                        if (node_A[0], node_B[0]) not in eqiv_nodes:
                            eqiv_nodes.append((node_A[0], node_B[0]))
                            if node_A in node_a_neighbours_no_previous:
                                node_a_neighbours_no_previous.remove(node_A)
                            if node_B in node_b_neighbours_no_previous:
                                node_b_neighbours_no_previous.remove(node_B)
                        else:
                            if node_A in node_a_neighbours_no_previous:
                                node_a_neighbours_no_previous.remove(node_A)
                            if node_B in node_b_neighbours_no_previous:
                                node_b_neighbours_no_previous.remove(node_B)
                    break
            if len(node_a_neighbours_no_previous) == 1 and  len(node_b_neighbours_no_previous) == 1:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
        #If neighbour list is of length 2 (after previously visited nodes removed)
        elif len_a_neigh == 2 and  len_b_neigh == 2:
            #First neighbour of Graph A compare with Graph B until match is found
            for node_A in node_a_neighbours_no_previous[:]:
                for node_B in node_b_neighbours_no_previous[:]:
                    if node_A[1] == node_B[1]:
                        if (node_A[0], node_B[0]) not in eqiv_nodes:
                            eqiv_nodes.append((node_A[0], node_B[0]))
                            if node_A in node_a_neighbours_no_previous:
                                node_a_neighbours_no_previous.remove(node_A)
                            if node_B in node_b_neighbours_no_previous:
                                node_b_neighbours_no_previous.remove(node_B)
                        else:
                            if node_A in node_a_neighbours_no_previous:
                                node_a_neighbours_no_previous.remove(node_A)
                            if node_B in node_b_neighbours_no_previous:
                                node_b_neighbours_no_previous.remove(node_B)
                    break
            if len(node_a_neighbours_no_previous) == 3 and  len(node_b_neighbours_no_previous) == 3:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
                nodes_need_changing.append((node_a_neighbours_no_previous[1], node_b_neighbours_no_previous[1], en[0], en[1]))
                nodes_need_changing.append((node_a_neighbours_no_previous[2], node_b_neighbours_no_previous[2], en[0], en[1]))
            if len(node_a_neighbours_no_previous) == 2 and  len(node_b_neighbours_no_previous) == 2:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
                nodes_need_changing.append((node_a_neighbours_no_previous[1], node_b_neighbours_no_previous[1], en[0], en[1]))
            if len(node_a_neighbours_no_previous) == 1 and  len(node_b_neighbours_no_previous) == 1:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
                
        #If neighbour list is of length 3 (after previously visited nodes removed)
        elif len_a_neigh == 3 and  len_b_neigh == 3:
            #First neighbour of Graph A compare with Graph B until match is found
            for node_A in node_a_neighbours_no_previous[:]:
                for node_B in node_b_neighbours_no_previous[:]:
                    if node_A[1] == node_B[1]:
                        if (node_A[0], node_B[0]) not in eqiv_nodes:
                            eqiv_nodes.append((node_A[0], node_B[0]))
                            if node_A in node_a_neighbours_no_previous:
                                node_a_neighbours_no_previous.remove(node_A)
                            if node_B in node_b_neighbours_no_previous:
                                node_b_neighbours_no_previous.remove(node_B)
                        else:
                            if node_A in node_a_neighbours_no_previous:
                                node_a_neighbours_no_previous.remove(node_A)
                            if node_B in node_b_neighbours_no_previous:
                                node_b_neighbours_no_previous.remove(node_B)
                    break
            if len(node_a_neighbours_no_previous) == 3 and  len(node_b_neighbours_no_previous) == 3:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
                nodes_need_changing.append((node_a_neighbours_no_previous[1], node_b_neighbours_no_previous[1], en[0], en[1]))
                nodes_need_changing.append((node_a_neighbours_no_previous[2], node_b_neighbours_no_previous[2], en[0], en[1]))
            if len(node_a_neighbours_no_previous) == 2 and  len(node_b_neighbours_no_previous) == 2:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
                nodes_need_changing.append((node_a_neighbours_no_previous[1], node_b_neighbours_no_previous[1], en[0], en[1]))
            if len(node_a_neighbours_no_previous) == 1 and  len(node_b_neighbours_no_previous) == 1:
                nodes_need_changing.append((node_a_neighbours_no_previous[0], node_b_neighbours_no_previous[0], en[0], en[1]))
        
        for node in nodes_need_changing[:]:
            node_a_id = node[0][0]
            node_a_type = node[0][1]
            node_a_parent = node[2]
            node_b_id = node[1][0]
            node_b_type = node[1][1]
            node_b_parent = node[3]
            neighbours_node_b = F_dict[node_b_id]['neighbours']
            if nodeValues[node_b_type].value > nodeValues[node_a_type].value:
                G_dict[node_a_id]['type'] = node_b_type
                G_dict[node_a_id]['neighbours'] = neighbours_node_b
                new_set_of_neighbours = []
                for neighbour in G_dict[node_a_parent]['neighbours']:
                    if neighbour[0] == node_a_id and neighbour[1] != node_b_type:
                        new_tuple = (node_a_id, node_b_type)
                        new_set_of_neighbours.append(new_tuple)                        
                    else:
                        new_tuple = (neighbour[0], neighbour[1])
                        new_set_of_neighbours.append(new_tuple)
                G_dict[node_a_parent]['neighbours'] = new_set_of_neighbours
                neighbours_for_new_node = []
                for neighbour in neighbours_node_b:
                    neighbours_for_new_node.append((node_a_id, node_a_type))
                    if neighbour[0] not in G_dict.keys():
                        G_dict[neighbour[0]] = {'neighbours' : [(node_a_id, node_b_type)], 'type': neighbour[1]}
            if nodeValues[node_b_type].value < nodeValues[node_a_type].value:
                #there is a new node to be added to the graph look at neighbours of new node, is one the node expected?
                for neighbour in neighbours_node_b[:]:
                    if neighbour == (node_b_parent, F_dict[node_b_parent]['type']):
                        neighbours_node_b.remove(neighbour)
                for neighbour in neighbours_node_b[:]:
                    if neighbour[1] == node_a_type:
                        neighbours_for_new_node = []
                        neighbours_for_new_node.append((node_a_parent, G_dict[node_a_parent]['type'])) #parent node
                        neighbours_for_new_node.append((node_a_id, node_a_type)) # expected node
                        for node in neighbours_node_b:
                            if node[0] not in G_dict.keys():
                                neighbours_for_new_node.append(node)
                                G_dict[node[0]] = {"type": node[1], 'neighbours': [(node_b_id, node_b_type)]}
                        G_dict[node_b_id] = {'type': node_b_type, 'neighbours': neighbours_for_new_node}
                        break
                    else:
                        dummy = 0
                old_parent_neigbours = G_dict[node_a_parent]['neighbours']
                new_set_of_neighbours = []
                for neighbour in old_parent_neigbours:
                    if (node_a_id, node_a_type) != neighbour:
                        new_tuple = (node_a_id, node_b_type)
                        new_set_of_neighbours.append(new_tuple)                        
                    else:
                        new_tuple = (node_b_id, node_b_type)
                        new_set_of_neighbours.append(new_tuple)
                G_dict[node_a_parent]['neigbours'] = new_set_of_neighbours

        nodes_need_changing.clear()
    edges = []
    for key in G_dict.keys():
        S.add_node(key)
        for neighbour in G_dict[key]['neighbours']:
            edge_tuple = (key, neighbour[0])
            if reversed(edge_tuple) not in edges:
                edges.append(edge_tuple)
    S.add_edges_from(edges)

    return S