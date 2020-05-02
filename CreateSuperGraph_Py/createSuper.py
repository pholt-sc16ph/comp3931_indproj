import os
import folderManagement as fM
import createGraph as cG
import findDiff as fD
import removeDummy as rD


def main():

    #return the folder name of the test to be used
    choice = input("Type '1' to run on test data, '2' to run on Tracsis test data or type '3' to run on Tracsis master data -> ")
    if choice == str(1):
        test_string = fM.return_test_name()
        path_to_folder = "../Data/automated_tests/"
        if fM.check_if_GMSCL_folder(test_string):
            print("Isomorphism check has been ran. Uncompressed data available for use")
            original_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/original_graph/Connectivity.xml")
            edited_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/edited_graph/Connectivity.xml")
            dummyless_ori = rD.remove_dummy(original_graph)
            dummyless_edi = rD.remove_dummy(edited_graph)
            # cG.display_graphs(dummyless_ori, dummyless_edi)
            fD.find_diff(dummyless_ori, dummyless_edi, "0", "0")
        else:
            print("No isomorphism check completed. Extracting usable files")
            fM.create_GMSCL_folder(test_string)
            original_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/original_graph/Connectivity.xml")
            edited_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/edited_graph/Connectivity.xml")
            dummyless_ori = rD.remove_dummy(original_graph)
            dummyless_edi = rD.remove_dummy(edited_graph)
            # cG.display_graphs(dummyless_ori, dummyless_edi)
            fD.find_diff(dummyless_ori, dummyless_edi, "0", "0")
    elif choice == str(2):
        test_string = fM.return_test_name_tracsis()
        path_to_folder = "../Data/tracsis_tests/"
        if fM.check_if_GMSCL_tracsis_test(test_string):
            print("Isomorphism check has been ran. Uncompressed data available for use")
            base_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/base_graph/Connectivity.xml")
            additional_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/additional_graph/Connectivity.xml")
            cG.display_graphs(base_graph, additional_graph)
        else:
            print("No isomorphism check completed. Extracting usable files")
            fM.create_GMSCL_tracsis_test(test_string)
            base_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/base_graph/Connectivity.xml")
            additional_graph = cG.create_graph(path_to_folder + test_string + "/GraphMatchingSoftware_CL/additional_graph/Connectivity.xml")
            cG.display_graphs(base_graph, additional_graph)

    elif choice == str(3):
        print("using Tracsis data")
        path = "C:/Users/peter/Source/Repos/pholt-sc16ph/comp3931_indproj/Data/tracsis_master_tests/GraphMatchingSoftware_CL/"
        if fM.check_if_GMSCL_tracsis():
            print("Isomorphism check has been ran. Uncompressed data available for use")
            inm_graph = cG.create_graph(path + "inm/Connectivity.xml")
            tps_graph = cG.create_graph(path + "tps/Connectivity.xml")
            # cG.create_graphviz_files(inm_graph, tps_graph, path)
        else:
            print("No isomorphism check completed. Extracting usable files")
            fM.create_GMSCL_tracsis()

            inm_graph = cG.create_graph(path + "inm/Connectivity.xml")
            tps_graph = cG.create_graph(path + "tps/Connectivity.xml")
            # cG.create_graphviz_files(inm_graph, tps_graph, path)
    else:
        print("please enter either '1', '2' or '3'")


if __name__ == '__main__':
    main()