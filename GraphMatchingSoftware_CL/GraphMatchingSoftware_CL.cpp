// GraphMatchingSoftware_CL.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <deque>
#include <iterator>
#include <string>
#include <set>
#include <exception>
#include "include/rapidxml/rapidxml.hpp"
#include "include/rapidxml/rapidxml_iterators.hpp"
#include "include/rapidxml/rapidxml_print.hpp"
#include "include/rapidxml/rapidxml_utils.hpp"
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/graph/isomorphism.hpp>
#include <boost/graph/vf2_sub_graph_iso.hpp>
#include <boost/graph/graph_utility.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/filesystem/directory.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/filesystem/convenience.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>
#include <boost/lexical_cast/lexical_cast_old.hpp>


using namespace std;
using namespace boost;
namespace pt = boost::property_tree;


using Graph = adjacency_list<vecS, vecS, undirectedS,
    property<vertex_name_t, string> >;

Graph create_empty_undirected_graph() { return {}; }

Graph create_graph(const vector<string>& names, const vector<boost::tuple<int, int>>& edges) noexcept {
    auto g = create_empty_undirected_graph();
    if (names.size() == 0) {
        return g;
    }

    auto vertex_name_map = get(vertex_name, g); // not boost::get

    auto vd_1 = add_vertex(g);
    vertex_name_map[vd_1] = *names.begin();
    if (names.size() == 1)
        return g;

    const auto j = std::end(names);
    auto name_it = std::begin(names);
    for (++name_it; name_it != j; ++name_it) // Skip first
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

//////////////////////////////////////// {{{
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
                    //std::cout << "Mapped '" << ins.first->first << "' to " << ins.first->second << "\n";
                }
            }
        }
    };


}
//////////////////////////////////////// }}}


int main() { 

    
    string path_to_tests = "../Data/automated_tests/";
    string test_in_directory = "0-dummy_1-switch_0-crossings_1-changes_116088/";
    string folder_in_tests = path_to_tests + test_in_directory;

    string GMS_CL_folder = "GraphMatchingSoftware_CL/";
    string original_folder = "original_graph/";
    string edited_folder = "edited_graph/";
    string original_graph_filename = "original_graph.orb";
    string edited_graph_filename = "edited_graph.orb";
    string original_graph_filename_zip = "original_graph.zip";
    string edited_graph_filename_zip = "edited_graph.zip";
    
    string con_xml = "Connectivity.xml";
    string path_to_orig_con_xml = folder_in_tests + GMS_CL_folder + original_folder + con_xml;
    string path_to_edit_con_xml = folder_in_tests + GMS_CL_folder + edited_folder + con_xml;
    boost::filesystem::path dir(folder_in_tests+GMS_CL_folder);
    if (boost::filesystem::create_directory(dir))
    {
        std::cerr << "Directory Created: " << std::endl;
    }

    boost::filesystem::path source_file_original = (folder_in_tests + original_graph_filename);
    boost::filesystem::path dest_file_original = (folder_in_tests + GMS_CL_folder + original_graph_filename_zip);
    boost::filesystem::copy_file(source_file_original, dest_file_original, boost::filesystem::copy_option::overwrite_if_exists);

    boost::filesystem::path source_file_edited = (folder_in_tests + edited_graph_filename);
    boost::filesystem::path dest_file_edited = (folder_in_tests + GMS_CL_folder + edited_graph_filename_zip);
    boost::filesystem::copy_file(source_file_edited, dest_file_edited, boost::filesystem::copy_option::overwrite_if_exists);

    const std::string XML_PATH1 = "./test.xml";
    const std::string DEFAULT_PART_NO = "XYZ";
    const std::string DEFAULT_ZIP = "90125";
    boost::property_tree::ptree pt1;
    boost::property_tree::read_xml(XML_PATH1, pt1);
    try
    {
        // Traverse property tree example
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, pt1.get_child("purchaseOrder.items"))
        {
            boost::property_tree::ptree subtree = node.second;

            if (node.first == "item")
            {
                BOOST_FOREACH(boost::property_tree::ptree::value_type const& v, subtree.get_child(""))
                {
                    std::string label = v.first;

                    if (label != "<xmlattr>")
                    {
                        std::string value = subtree.get<std::string>(label);
                        //std::cout << label << ":  " << value << std::endl;
                    }
                }
                //std::cout << std::endl;
            }
        }
    }
    catch (std::exception& e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }

    const std::string XML_PATH_ORIG = path_to_orig_con_xml;
    vector<string> nodes_original;
    vector<boost::tuple<int, int>> edges_original;
    boost::property_tree::ptree or_conn;
    boost::property_tree::read_xml(XML_PATH_ORIG, or_conn);
    std::cout << "\n" + original_folder + con_xml << "\n";
    try 
    {
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, or_conn.get_child("Connectivity.Nodes"))
        {
            boost::property_tree::ptree subtree = node.second;
            std::string node_label = node.second.get_child("<xmlattr>.id").data();
            BOOST_FOREACH(boost::property_tree::ptree::value_type const& v, subtree.get_child(""))
            {
                std::cout <<"Nodes: " << node_label;
                nodes_original.push_back(node_label);
            }
            std::cout << std::endl;
        }
        std::cout << "\n";
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, or_conn.get_child("Connectivity.TrackSections"))
        {
            boost::property_tree::ptree subtree = node.second;
            std::string start_node = node.second.get_child("<xmlattr>.startNode").data();
            std::string end_node = node.second.get_child("<xmlattr>.endNode").data();
            BOOST_FOREACH(boost::property_tree::ptree::value_type const& v, subtree.get_child(""))
            {
                std::cout <<"Edges: " << start_node << " -> " << end_node;
                stringstream temp_start(start_node);
                int start_node_int = 0;
                temp_start >> start_node_int;
                stringstream temp_end(end_node);
                int end_node_int = 0;
                temp_end >> end_node_int;
                edges_original.push_back(boost::tuple<int, int>(start_node_int, end_node_int));
            }
            std::cout << std::endl;
        }
    }
    catch (std::exception& e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }

    const std::string XML_PATH_EDIT = path_to_edit_con_xml;
    vector<string> nodes_edited;
    vector<boost::tuple<int, int>> edges_edited;
    boost::property_tree::ptree ed_conn;
    boost::property_tree::read_xml(XML_PATH_EDIT, ed_conn);
    std::cout << "\n" + edited_folder + con_xml << "\n";
    try
    {
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, ed_conn.get_child("Connectivity.Nodes"))
        {
            boost::property_tree::ptree subtree = node.second;
            std::string node_label = node.second.get_child("<xmlattr>.id").data();
            BOOST_FOREACH(boost::property_tree::ptree::value_type const& v, subtree.get_child(""))
            {
                std::cout << "Nodes: " << node_label;
                nodes_edited.push_back(node_label);
            }
            std::cout << std::endl;
        }
        std::cout << "\n";
        BOOST_FOREACH(boost::property_tree::ptree::value_type const& node, ed_conn.get_child("Connectivity.TrackSections"))
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
                edges_edited.push_back(boost::tuple<int, int>(start_node_int, end_node_int));
            }
            std::cout << std::endl;
        }
    }
    catch (std::exception& e)
    {
        std::cout << "Error: " << e.what() << "\n";
    }  

    /*const auto original = create_graph(nodes_original, edges_original);
    const auto edited = create_graph(nodes_original, edges_original);
    ofstream ofso("original.dot");
    write_graphviz(ofso, original);
    ofstream ofse("edited.dot");
    write_graphviz(ofse, edited);*/
    
    const auto original = create_graph(nodes_original, edges_original);
    const auto edited = create_graph(nodes_edited, edges_edited);
    ofstream ofso("original.dot");
    write_graphviz(ofso, original);
    ofstream ofse("edited.dot");
    write_graphviz(ofse, edited);

    if (boost::isomorphism(original, edited)) {
        std::cout << "\nGraphs are isomorphic returning from program. Either data set is valid as there are no differences between them\n";
        return 0;
    }
    else {
        std::cout << "\nGraphs are different performing check to create super graph\n";
        return 0;
    }

    
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