// GraphMatchingSoftware_CL.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <deque>
#include <iterator>
#include <string>
#include <set>
#include <exception>
#include <fstream>
#include <stdlib.h>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/graph/isomorphism.hpp>
#include <boost/graph/vf2_sub_graph_iso.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/filesystem.hpp>
#include <boost/filesystem/directory.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/convenience.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>

#include "constants.h"

using namespace std;
using namespace boost;
namespace pt = boost::property_tree;
typedef std::vector<std::string> stringvec;

using Graph = adjacency_list<vecS, vecS, undirectedS,
    property<vertex_name_t, string> >;

Graph create_empty_undirected_graph() { return {}; }

Graph create_graph(const vector<string>& names, const vector<boost::tuple<int, int>>& edges) noexcept {
    auto g = create_empty_undirected_graph();
    if (names.size() == 0) {
        return g;
    }

    auto vertex_name_map = get(vertex_name, g); 

    auto vd_1 = add_vertex(g);
    vertex_name_map[vd_1] = *names.begin();
    if (names.size() == 1)
        return g;

    const auto j = std::end(names);
    auto name_it = std::begin(names);
    for (++name_it; name_it != j; ++name_it) 
    {
        auto vd_2 = add_vertex(g);
        vertex_name_map[vd_2] = *name_it;
        vd_1 = vd_2;
    }

    for (int i = 0; i < edges.size(); i++)
    {
        boost::tuple<int, int> edge_tuple = edges[i];
        int edge_one = get<0>(edge_tuple);
        int edge_two = get<1>(edge_tuple);
        add_edge(edge_one, edge_two, g);
    }
    return g;
}
//define the name space for vertex identification
namespace {
    struct VertexInvariant {
        using Map = map<string, size_t>;
        Graph const& _graph;
        Map& _mappings;

        using result_type = size_t;
        using argument_type = Graph::vertex_descriptor;

        size_t operator()(argument_type u) const {
            return _mappings.at(get(vertex_name, _graph, u));
        }
        size_t max() const { return _mappings.size(); }

        void collect_names() {
            for (auto vd : make_iterator_range(vertices(_graph))) {
                size_t next_id = _mappings.size();
                auto ins = _mappings.insert({ get(vertex_name, _graph, vd), next_id });
                if (ins.second) {
                }
            }
        }
    };
}
//create nodes reads the Nodes section of the "Connectivity.xml" file of supplied .orb files
vector<string> createNodes(string path_to_file) {
    vector<string> nodes;
    boost::property_tree::ptree conn;
    boost::property_tree::read_xml(path_to_file, conn);
    try
    {
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, conn.get_child("Connectivity.Nodes"))
        {
            boost::property_tree::ptree subtree = node.second;
            std::string node_label = node.second.get_child("<xmlattr>.id").data();
            BOOST_FOREACH(boost::property_tree::ptree::value_type const& v, subtree.get_child(""))
            {
                std::cout << "Nodes: " << node_label;
                nodes.push_back(node_label);
            }
            std::cout << std::endl;
        }
        std::cout << "\n";
    }
    catch (std::exception& e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }
    return nodes;
}
//create edges reads the TrackSections section of the "Connectivity.xml" file of supplied .orb files
vector<boost::tuple<int, int>> createEdges(string path_to_file) {
    vector<boost::tuple<int, int>> edges;
    edges.reserve(50000);
    boost::property_tree::ptree conn;
    boost::property_tree::read_xml(path_to_file, conn);
    try
    {
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, conn.get_child("Connectivity.TrackSections"))
        {
            boost::property_tree::ptree subtree = node.second;
            std::string start_node = node.second.get_child("<xmlattr>.startNode").data();
            std::string end_node = node.second.get_child("<xmlattr>.endNode").data();
            BOOST_FOREACH(boost::property_tree::ptree::value_type const& v, subtree.get_child(""))
            {
                std::cout << "Edges: " << start_node << " -> " << end_node;
                stringstream temp_start(start_node);
                int start_node_int = 0;
                temp_start >> start_node_int;
                stringstream temp_end(end_node);
                int end_node_int = 0;
                temp_end >> end_node_int;
                edges.push_back(boost::tuple<int, int>(start_node_int, end_node_int));
            }
            std::cout << std::endl;
        }
        std::cout << "\n";
    }
    catch (std::exception& e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }
    return edges;
}
//read the directory
struct path_leaf_string
{
    std::string operator()(const boost::filesystem::directory_entry& entry) const
    {
        return entry.path().leaf().string();
    }
};
void read_directory(const std::string& name, stringvec& v)
{
    boost::filesystem::path p(name);
    boost::filesystem::directory_iterator start(p);
    boost::filesystem::directory_iterator end;
    std::transform(start, end, std::back_inserter(v), path_leaf_string());
}


int main() {
    stringvec v;
    read_directory("../Data/automated_tests/", v);
    int x = 0;
    for (auto it = std::begin(v); it != std::end(v); ++it) {
        std::cout << "Index: " + std::to_string(x)+ " || Test Name: " + *it << "\n";
        x++;
    }
    if (v.empty()) {
        std::cout << "No vector of tests. Please create a test from /CreateTestGraphs_Py directory by running 'python create.py' and try again\nClosing program...";
        return 0;
    }

    int num;
    std::string test_selected;
    std::cout << "Please enter the index number of the test you would like to select: ";
    cin >> num;
    
    if (num > x) {
        std::cout << "Index selected doesn't exist. Please run the program again and select a valid test";
        return 0;
    }
    else if (cin.fail()) {
        std::cout << "Please enter an integer value from the index list";
        return 0;
    }
    else {
        std::string test_selected = v.at(num);

        
        //create the GMS_CL folder in the specifed automated_tests folder. As it stands the specific test is hardcoded in constants.h
        boost::filesystem::path dir(constants::PATH_TO_TESTS + test_selected + constants::GMS_CL_FOLDER);
        boost::filesystem::create_directory(dir);
        stringvec GMS_dir;
        read_directory("../Data/automated_tests/" + test_selected + constants::GMS_CL_FOLDER, GMS_dir);

        if (GMS_dir.empty()) {
            //copy the .orb files from the test folder into the newly created GMS_CL folder for manipulation
            boost::filesystem::copy_file(constants::PATH_TO_TESTS + test_selected + constants::ORIGINAL_GRAPH_FILENAME, constants::PATH_TO_TESTS + test_selected + constants::GMS_CL_FOLDER + constants::ORIGINAL_GRAPH_FILENAME_ZIP, boost::filesystem::copy_option::overwrite_if_exists);
            boost::filesystem::copy_file(constants::PATH_TO_TESTS + test_selected + constants::EDITED_GRAPH_FILENAME, constants::PATH_TO_TESTS + test_selected + constants::GMS_CL_FOLDER + constants::EDITED_GRAPH_FILENAME_ZIP, boost::filesystem::copy_option::overwrite_if_exists);

            //extract heirachy structure from .zip file and place in GMS_CL folder. Using scripts and batch file to complete this to save time.
            ofstream batch;
            batch.open("extract.bat", ios::out);
            batch << "Powershell Expand-Archive -Path '../Data/automated_tests/" + test_selected + "/GraphMatchingSoftware_CL/original_graph.zip' -DestinationPath ../Data/automated_tests/" + test_selected + "/GraphMatchingSoftware_CL/original_graph\n";
            batch << "Powershell Expand-Archive -Path '../Data/automated_tests/" + test_selected + "/GraphMatchingSoftware_CL/edited_graph.zip' -DestinationPath ../Data/automated_tests/" + test_selected + "/GraphMatchingSoftware_CL/edited_graph\n";
            batch.close();
            std::system("extract.bat");
            std::remove("extract.bat");
        }


        //create vector to hold the nodes derived from test Connectivity.xml file from original
        vector<string> nodesOriginal = createNodes(constants::PATH_TO_TESTS + test_selected + constants::PATH_TO_ORIGINAL_CON_XML);
        //create vector to hold edges derived from test Connectivity.xml file from original
        vector<boost::tuple<int, int>> edgesOriginal = createEdges(constants::PATH_TO_TESTS + test_selected + constants::PATH_TO_ORIGINAL_CON_XML);
        //create graph for use with isomorphism function and to create .dot file to view graph in gvedit
        const auto original = create_graph(nodesOriginal, edgesOriginal);
        ofstream ofso("original.dot");
        write_graphviz(ofso, original);

        //create vector to hold the nodes derived from test Connectivity.xml file from edited
        vector<string> nodesEdited = createNodes(constants::PATH_TO_TESTS + test_selected + constants::PATH_TO_EDITED_CON_XML);
        //create vector to hold edges derived from test Connectivity.xml file from edited
        vector<boost::tuple<int, int>> edgesEdited = createEdges(constants::PATH_TO_TESTS + test_selected + constants::PATH_TO_EDITED_CON_XML);
        //create graph for use with isomorphism function and to create .dot file to view graph in gvedit
        const auto edited = create_graph(nodesEdited, edgesEdited);
        ofstream ofse("edited.dot");
        write_graphviz(ofse, edited);

        if (boost::isomorphism(original, edited)) {
            std::cout << "\nGraphs are isomorphic returning from program. Either data set is valid as there are no differences between them\n";
            return 0;
        }
        else {
            std::cout << "\nGraphs are different. Performing check to create super graph\n";
            return 0;
        }
    };
}


// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file