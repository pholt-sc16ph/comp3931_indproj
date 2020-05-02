import json
"""
Methods to keep track of the changes made between the original graph and the edited graph
"""
def print_info(dictionary):
    """Print to terminal

  Args:
    dictionary (dict): Dictionary of changes

  Returns:
    void:
  """
    print(json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': ')))

def write_json_file(dictionary, path):
    """Print to json file for future parsing

  Args:
    dictionary (dict): Dictionary of changes

  Returns:
    void:
  """
    path_to_save = path + "/changes.json"
    file = open(path_to_save, 'w+')
    file.write(json.dumps(dictionary, sort_keys=True, indent=4))
    file.close()
    return

def write_text_file(dictionary, path):
    """Print to human readable text file

  Args:
    dictionary (dict): Dictionary of changes

  Returns:
    void:
  """
    dict_to_extract = dictionary
    string_array = []
    for key in dict_to_extract:
        #string
        change_number = str(key)
        #string
        #["swapwithlimit", "adddummynode", "swapwithdummynode", "swapwithswitchnode", "swapwithcrossingnode", "deletenode"]
        action = dict_to_extract[key]['action_completed']
        if action == "swapwithlimit":
            action = "Swap with LimitOfNetwork"
        elif action == "adddummynode":
            action = "Add DummyNode"
        elif action == "swapwithdummynode":
            action = "Swap with DummyNode"
        elif action == "swapwithswitchnode":
            action = "Swap with Switch"
        elif action == "swapwithcrossingnode":
            action = "Swap with FlatCrossing"
        elif action == "deletenode":
            action = "Delete node"
        
        #tuple
        node_acted_upon = str(dict_to_extract[key]['node_acted_upon'])
        #tuple
        node_swapped_or_added = str(dict_to_extract[key]['node_swapped_or_added'])
        #array of tuples
        nodes_created = dict_to_extract[key]['nodes_created']
        array_of_created_nodes_strings = []
        for item in nodes_created:
            array_of_created_nodes_strings.append(str(item))
        nodes_created_string = " "
        for item in array_of_created_nodes_strings:
            nodes_created_string+=str(item)
        #array of tuples
        nodes_deleted = dict_to_extract[key]['nodes_deleted']
        array_of_deleted_nodes_strings = []
        for item in nodes_deleted:
            array_of_deleted_nodes_strings.append(str(item))
        nodes_deleted_string = " "
        for item in array_of_deleted_nodes_strings:
            nodes_deleted_string+=str(item)

        # print(key, '->', dict_to_extract[key])
        string_to_add_to_array = ("Change Number: " + str(key) + 
                                  " -- Action Taken: " + action + 
                                  " || Node Changed: " + node_acted_upon + 
                                  " || Node Swapped With: " + node_swapped_or_added + 
                                  " || Nodes Created: " + nodes_created_string + 
                                  " || Nodes Deleted: " + nodes_deleted_string + "\n\n" )
        
        string_array.append(string_to_add_to_array)
        # print(key+action+node_acted_upon+node_swapped_or_added+nodes_created_string+nodes_deleted_string)
    

    path_to_save = path + "/changes.txt"
    file = open(path_to_save, 'w+')
    for item in string_array:
        file.write(item)
    file.close()
    return