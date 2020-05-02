import networkx as nx
import json



def find_diff(base, additional, start_node_base, start_node_add):
    G = base
    F = additional
    S = nx.Graph()
    sG = start_node_base
    sF = start_node_add

    G_dict = {}
    F_dict = {}
    S_dict = {}

    for node in G:
        neighbours = []
        print("node: " + node + " " + str(G.edges(node)))
        print("node: " + node + " " + str(list(G[node])))
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
    # print(eqiv_nodes)
    nodes_need_changing = []
    # for en in eqiv_nodes:
    #     node_a = en[0]
    #     node_b = en[1]
    #     node_a_neighbours = G_dict[node_a]['neighbours']
    #     node_b_neighbours = F_dict[node_b]['neighbours']
    #     len_a_neigh = len(node_a_neighbours)
    #     len_b_neigh = len(node_b_neighbours)
    #     print("Node a neighbours: " + str(node_a_neighbours) + " length: " + str(len_a_neigh))
    #     print("Node b neighbours: " + str(node_b_neighbours) + " length: " + str(len_b_neigh))    
    #     if len_a_neigh == 1 and  len_b_neigh == 1:
    #         if node_a_neighbours[0][1] == node_b_neighbours[0][1]:
    #             eqiv_nodes.append((node_a_neighbours[0][0], node_b_neighbours[0][0]))
    #         elif node_a_neighbours[0][1] != node_b_neighbours[0][1]:
    #             nodes_need_changing.append((node_a_neighbours[0][0], node_b_neighbours[0][0]))
    #     #don't need to check 2, dummies should have been removed
    #     if len_a_neigh == 3 and len_b_neigh == 3:
    #         if node_a_neighbours[1][1] == node_b_neighbours[1][1]:
    #             eqiv_nodes.append((node_a_neighbours[1][0], node_b_neighbours[1][0]))
    #         elif node_a_neighbours[1][1] == node_b_neighbours[2][1]:
    #             eqiv_nodes.append((node_a_neighbours[1][0], node_b_neighbours[2][0]))
    #     print(eqiv_nodes)
    # print(eqiv_nodes)
    # print(nodes_need_changing)

    # print("\nGraph G \n" + json.dumps(G_dict, sort_keys=True, indent=4))
    # print("\nGraph F \n" + json.dumps(F_dict, sort_keys=True, indent=4))
    
    file = open("G.json", 'w+')
    file.write(json.dumps(G_dict, sort_keys=False, indent=4))
    file.close()
    file = open("F.json", 'w+')
    file.write(json.dumps(F_dict, sort_keys=False, indent=4))
    file.close()
    return S