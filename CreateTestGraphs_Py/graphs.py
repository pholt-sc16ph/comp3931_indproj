#create a graph from user input, user will decide the number of nodes and edges

import networkx as nx


#initailise graph, input variables and arrays to hold string representation of nodes
G = nx.Graph()
limit_number = None
switch_number = None
crossing_number = None
limit_array = []
switch_array = []
crossing_array = []
complete_node_array = []

#get user input 
while True:
    limit_number = 6
    switch_number = 2
    crossing_number = 1
    # limit_number = input ("Choose number of limit of network nodes: ")
    # switch_number = input ("Choose number of switch nodes: ")
    # crossing_number = input ("Choose number of crossing nodes: ")
    break    

for i in range(int(limit_number)):
    limit_array.append("lm_" + str(i))       
for i in range(int(switch_number)):
    switch_array.append("sw_" + str(i))
for i in range(int(crossing_number)):
    crossing_array.append("cr_" + str(i))



for i in range(int(limit_number)):
    G.add_node(limit_array[i], type = "limit")       
for i in range(int(switch_number)):
    G.add_node(switch_array[i], type = "switch")
for i in range(int(crossing_number)):
    G.add_node(crossing_array[i], type = "crossing")

# G.add_nodes_from(complete_node_array)

print("\nPrint nodes of graph: " + str(G.nodes().data()) + "\n")
# print(G.nodes[1])







   
    


