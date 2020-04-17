import networkx as nx
import matplotlib.pyplot as plt
import random


changes_dict = {}


def graph_edit(graph, no_of_changes):
    F = graph
    
    list_of_nodes = list(F.nodes())    
    for x in range(0, no_of_changes):
        temp_dict = {}
        random_node = random.choice(list_of_nodes)

        #for record keeping
        random_node_type = F.nodes[random_node]['type']
        random_node_info_for_dict = (random_node, random_node_type)
        list_of_nodes_added_during_change = []
        list_of_nodes_deleted_during_change = []
        #end of record keeping
        
        random_node_degree = F.degree(random_node)
        list_of_nodes.remove(random_node)
        number_of_nodes = F.number_of_nodes()
        random_node_neighbors = list(F.neighbors(random_node))
        random_choice_list = ["swapwithlimit", "adddummynode", "swapwithdummynode", "swapwithswitchnode", "swapwithcrossingnode", "deletenode"]
        random_action = random.choice(random_choice_list)

        #code for adding to dictionary for record keeping
        temp_dict['action_completed'] = random_action
        temp_dict['node_acted_upon'] = random_node_info_for_dict
        #end of record keeping

        if random_action == "swapwithlimit":
            F.remove_node(random_node)
            lost_nodes = []
            for node in F:
                    if F.degree(node) == 0:
                        lost_nodes.append(node)
            if len(lost_nodes) > 0:
                    for item in lost_nodes:
                        #code for adding to dictionary for record keeping
                        deleted_node_type = F.nodes[item]['type']
                        deleted_node_info_for_dict = (item, deleted_node_type)
                        list_of_nodes_deleted_during_change.append(deleted_node_info_for_dict)
                        #end of record keeping
                        F.remove_node(item)
                        random_node_neighbors.remove(item)

            F.add_node(random_node, type="LimitOfNetwork")
            random_node_type = F.nodes[random_node]['type']
            random_node_info_for_dict = (random_node, random_node_type)
            temp_dict['node_swapped_or_added'] = random_node_info_for_dict
            F.add_edge(random_node, random.choice(random_node_neighbors))
        if random_action == "adddummynode":
            choose_random_neighbour = random.choice(random_node_neighbors)
            F.remove_edge(random_node, choose_random_neighbour)
            new_node = number_of_nodes
            F.add_node(new_node, type="DummyNode")
            random_node_type = F.nodes[new_node]['type']
            random_node_info_for_dict = (new_node, random_node_type)
            temp_dict['node_swapped_or_added'] = random_node_info_for_dict
            F.add_edge(new_node, random_node)
            F.add_edge(new_node, choose_random_neighbour)
        if random_action == "swapwithdummynode":
            if len(random_node_neighbors) > 1:
                F.remove_node(random_node)
                F.add_node(random_node, type="DummyNode")
                random_node_type = F.nodes[random_node]['type']
                random_node_info_for_dict = (random_node, random_node_type)
                temp_dict['node_swapped_or_added'] = random_node_info_for_dict
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
            elif len(random_node_neighbors) == 1:
                F.remove_node(random_node)
                F.add_node(random_node, type="DummyNode")

                #code for adding to dictionary for record keeping
                random_node_type = F.nodes[random_node]['type']
                random_node_info_for_dict = (random_node, random_node_type)
                temp_dict['node_swapped_or_added'] = random_node_info_for_dict
                #end of record keeping

                original_neighbor = random_node_neighbors[0]
                new_node = number_of_nodes
                F.add_node(new_node, type="LimitOfNetwork")

                #code for adding to dictionary for record keeping
                new_node_type = F.nodes[new_node]['type']
                new_node_info_for_dict = (new_node, new_node_type)
                list_of_nodes_added_during_change.append(new_node_info_for_dict)
                #end of record keeping

                F.add_edge(random_node, original_neighbor)
                F.add_edge(random_node, new_node)
            lost_nodes = []
            for node in F:
                    if F.degree(node) == 0:
                        lost_nodes.append(node)
            if len(lost_nodes) > 0:
                    for item in lost_nodes:
                        #code for adding to dictionary for record keeping
                        deleted_node_type = F.nodes[item]['type']
                        deleted_node_info_for_dict = (item, deleted_node_type)
                        list_of_nodes_deleted_during_change.append(deleted_node_info_for_dict)
                        #end of record keeping
                        F.remove_node(item)
        if random_action == "swapwithswitchnode":
            if len(random_node_neighbors) == 1:
                F.remove_node(random_node)
                F.add_node(random_node, type="Switch")

                #code for adding to dictionary for record keeping
                random_node_type = F.nodes[random_node]['type']
                random_node_info_for_dict = (random_node, random_node_type)
                temp_dict['node_swapped_or_added'] = random_node_info_for_dict
                #end of record keeping

                original_neighbor = random_node_neighbors[0]
                new_node = number_of_nodes
                new_node_plus_one = number_of_nodes + 1
                F.add_node(new_node, type="LimitOfNetwork")
                F.add_node(new_node_plus_one, type="LimitOfNetwork")

                #code for adding to dictionary for record keeping
                new_node_type = F.nodes[new_node]['type']
                new_node_info_for_dict1 = (new_node, new_node_type)
                new_node_type = F.nodes[new_node_plus_one]['type']
                new_node_info_for_dict2 = (new_node_plus_one, new_node_type)
                list_of_nodes_added_during_change.append(new_node_info_for_dict1)
                list_of_nodes_added_during_change.append(new_node_info_for_dict2)
                #end of record keeping

                F.add_edge(random_node, original_neighbor)
                F.add_edge(random_node, new_node)
                F.add_edge(random_node, new_node_plus_one)
            if len(random_node_neighbors) == 2:
                F.remove_node(random_node)
                F.add_node(random_node, type="Switch")
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                new_node = number_of_nodes
                F.add_node(new_node, type="LimitOfNetwork")
                F.add_edge(random_node, new_node)
            if len(random_node_neighbors) == 3:
                #already a switch no point completing computation
                dummy = 0
            if len(random_node_neighbors) == 4:
                F.remove_node(random_node)
                F.add_node(random_node, type="Switch")
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
        #if 5 swap with crossing node
        if random_action == "swapwithcrossingnode":
            if len(random_node_neighbors) == 1:
                F.remove_node(random_node)
                F.add_node(random_node, type="FlatCrossing")
                original_neighbor = random_node_neighbors[0]
                new_node = number_of_nodes
                new_node_plus_one = number_of_nodes + 1
                new_node_plus_two = number_of_nodes + 2
                F.add_node(new_node, type="LimitOfNetwork")
                F.add_node(new_node_plus_one, type="LimitOfNetwork")
                F.add_node(new_node_plus_two, type="LimitOfNetwork")
                F.add_edge(random_node, original_neighbor)
                F.add_edge(random_node, new_node)
                F.add_edge(random_node, new_node_plus_one)
                F.add_edge(random_node, new_node_plus_two)
            if len(random_node_neighbors) == 2:
                F.remove_node(random_node)
                F.add_node(random_node, type="FlatCrossing")
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                new_node = number_of_nodes
                new_node_plus_one = number_of_nodes + 1
                F.add_node(new_node_plus_one, type="LimitOfNetwork")
                F.add_node(new_node, type="LimitOfNetwork")
                F.add_edge(random_node, new_node)
                F.add_edge(random_node, new_node_plus_one)
            if len(random_node_neighbors) == 3:
                F.remove_node(random_node)
                F.add_node(random_node, type="FlatCrossing")
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                random_node_neighbors.remove(choose_random_neighbour)
                choose_random_neighbour = random.choice(random_node_neighbors)
                F.add_edge(random_node, choose_random_neighbour)
                new_node = number_of_nodes
                F.add_node(new_node, type="LimitOfNetwork")
                F.add_edge(random_node, new_node)
            if len(random_node_neighbors) == 4:
                #already a crossing so no need to complete computation
                dummy = 0
        #if 6 just remove node
        if random_action == "deletenode":
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
        # print("Remove nodes which satisfy type and degree")
        for node in F:
            if F.nodes[node]['type'] == 'Switch' and F.degree[node] == 3:
                # print("Remove: G.nodes[node]['type'] == 'Switch' and G.degree[node] == 3")
                if node in list_of_nodes:
                    list_of_nodes.remove(node)
            elif F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 4:
                # print("Remove: G.nodes[node]['type'] == 'FlatCrossing' and G.degree[node] == 4")
                if node in list_of_nodes:
                    list_of_nodes.remove(node)
            elif F.nodes[node]['type'] == 'DummyNode' and F.degree[node] == 2:
                # print("Remove: G.nodes[node]['type'] == 'DummyNode' and G.degree[node] == 2")
                if node in list_of_nodes:
                    list_of_nodes.remove(node)
    temp_dict["nodes_created"] = list_of_nodes_added_during_change
    temp_dict["nodes_deleted"] = list_of_nodes_deleted_during_change
    changes_dict[x+1] = temp_dict

    add_limit_node_number = len(F.nodes())
    # print("Adding LimitOFNetwork to nodes whcih dont have the correct degree for their type")
    for node in list_of_nodes:
        node
        if F.nodes[node]['type'] == 'DummyNode' and F.degree[node] == 1:
            # print("F.nodes[node]['type'] == 'DummyNode' and F.degree[node] == 1")
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif F.nodes[node]['type'] == 'Switch' and F.degree[node] == 1:
            # print("F.nodes[node]['type'] == 'Switch' and F.degree[node] == 1")
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif F.nodes[node]['type'] == 'Switch' and F.degree[node] == 2:
            # print("F.nodes[node]['type'] == 'Switch' and F.degree[node] == 2")
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 1:
            # print("F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 1")
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 2:
            # print("F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 2")
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
        elif F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 3:
            # print("F.nodes[node]['type'] == 'FlatCrossing' and F.degree[node] == 3")
            F.add_node(add_limit_node_number, type="LimitOfNetwork")
            F.add_edge(node, add_limit_node_number)
            add_limit_node_number += 1
    
    
    """
    # catch if node zero was deleted. Clear the graph and populate with one node, node zero
    for node in F:
        list_of_end_process = []
        list_of_end_process.append(node)
    if 0 not in list_of_end_process:
        F.clear()
        F.add_node(0, type="LimitOfNetwork")
    
    # catch if deleting a node caused a cluster of node tp be separated from the main group. this cluster needs deleting
    deleted_nodes_cluster = []
    for node in F:
        if node not in nx.node_connected_component(F, 0):
            deleted_nodes_cluster.append(node)
    if not deleted_nodes_cluster:
        F.remove_nodes_from(deleted_nodes_cluster)

    """
    F.nodes(data=True)
    """ Graph data for edited graph"""
    """
    print("Data and graph for F")
    print(nx.node_connected_component(F, 0))
    print(deleted_nodes_cluster)
    print(nx.number_connected_components(F))
    print(nx.info(F))
    print("\n")
    """

    return F


