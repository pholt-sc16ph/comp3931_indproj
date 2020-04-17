import json

changes_dict = {}

x = {}

random_node = 8
random_node_type = "Switch"

random_node_info = (random_node, random_node_type)
x["node_acted_upon"] = random_node_info
new_node = 8
new_node_type = "DummyNode"
new_node_info = (new_node, new_node_type)
x["node_swapped_with"] = new_node_info

testlistadded = [(4, "LimitOfNetwork"), (5, "LimitOfNetwork"), (6, "LimitOfNetwork")]
x["nodes_created"] = testlistadded
testlistdeleted = [(7, "Switch"), (8, "FlatCrossing"), (9, "FlatCrossing")]
x["nodes_deleted"] = testlistdeleted




x2 ={}

random_node2 = 8
random_node_type2 = "Switch"

random_node_info2 = (random_node2, random_node_type2)
x2["node_acted_upon"] = random_node_info
new_node2 = 8
new_node_type2 = "DummyNode"
new_node_info2 = (new_node2, new_node_type2)
x2["node_swapped_with"] = new_node_info
testlistadded2 = [(4, "LimitOfNetwork"), (5, "LimitOfNetwork"), (6, "LimitOfNetwork")]
x2["nodes_created"] = testlistadded
testlistdeleted2 = [(7, "Switch"), (8, "FlatCrossing"), (9, "FlatCrossing")]
x2["nodes_deleted"] = testlistdeleted

changes_dict[1] = x
changes_dict[2] = x2
print(json.dumps(
    changes_dict,
    sort_keys=True,
    indent=4,
))
