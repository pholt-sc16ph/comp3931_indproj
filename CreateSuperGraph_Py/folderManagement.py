import os
import shutil
import zipfile



def return_test_name():
    """return a list of the folders in automated_tests directory
  
  Returns:
    List: list of directories containing tests
  """
    list_of_tests = os.listdir("../Data/automated_tests")
    

    for item in list_of_tests:
        print("Index no: " + str(list_of_tests.index(item)) + " || Test name: " + item)

    choice = input ("Choose test from list above: ")
    test_chosen = list_of_tests[int(choice)]

    return test_chosen

def return_test_name_tracsis():
    """return a list of the folders in tracsis_tests directory
  
  Returns:
    List: list of directories containing tests
  """
    list_of_tests = os.listdir("../Data/tracsis_tests")
    

    for item in list_of_tests:
        print("Index no: " + str(list_of_tests.index(item)) + " || Test name: " + item)

    choice = input ("Choose test from list above: ")
    test_chosen = list_of_tests[int(choice)]

    return test_chosen

def check_if_GMSCL_folder(test):
    """Check to see if folder containing XML files is present
  Args:
    test (String): the directory chosen by the user
    
  Returns:
    Boolean: True if folder present and false if folder missing
  """
    path = 'C:/Users/peter/Source/Repos/pholt-sc16ph/comp3931_indproj/Data/automated_tests/' + test + '/GraphMatchingSoftware_CL'
    return os.path.isdir(path)

def check_if_GMSCL_tracsis_test(test):
    """Check to see if folder containing XML files is present
  Args:
    test (String): the directory chosen by the user
    
  Returns:
    Boolean: True if folder present and false if folder missing
  """
    path = 'C:/Users/peter/Source/Repos/pholt-sc16ph/comp3931_indproj/Data/tracsis_tests/' + test + '/GraphMatchingSoftware_CL'
    return os.path.isdir(path)

def check_if_GMSCL_tracsis():
    """Check to see if folder containing XML files is present
  Args:
    test (String): the directory chosen by the user
    
  Returns:
    Boolean: True if folder present and false if folder missing
  """
    path = 'C:/Users/peter/Source/Repos/pholt-sc16ph/comp3931_indproj/Data/tracsis_master_tests/GraphMatchingSoftware_CL'
    return os.path.isdir(path)


def create_GMSCL_folder(test):
    """Creates XML files from .orb files and places in folders in automated_tests folder
  Args:
    test (String): the directory chosen by the user
    

  Returns:
    Void: 
  """
    os.mkdir("../Data/automated_tests/" + test + "/GraphMatchingSoftware_CL")
    shutil.copyfile("../Data/automated_tests/" + test + "/original_graph.orb", "../Data/automated_tests/" + test + "/GraphMatchingSoftware_CL/original_graph.orb")
    shutil.copyfile("../Data/automated_tests/" + test + "/edited_graph.orb", "../Data/automated_tests/" + test + "/GraphMatchingSoftware_CL/edited_graph.orb")
    filenames = ["original_graph.orb", "edited_graph.orb"]
    path = "../Data/automated_tests/" + test + "/GraphMatchingSoftware_CL/"
    for filename in filenames:
        directory = filename.split(".")
        zfName = filename
        pre, ext = os.path.splitext(path+zfName)
        os.rename(path+zfName, pre + ".zip")
        zfName = pre + ".zip"
        with zipfile.ZipFile(zfName, 'r') as zip_ref:
            zip_ref.extractall(path + directory[0])

def create_GMSCL_tracsis_test(test):
    """Creates XML files from .orb files and places in folders in tracsis_tests folder
  Args:
    test (String): the directory chosen by the user
    

  Returns:
    Void: 
  """
    os.mkdir("../Data/tracsis_tests/" + test + "/GraphMatchingSoftware_CL")
    shutil.copyfile("../Data/tracsis_tests/" + test + "/base_graph.orb", "../Data/tracsis_tests/" + test + "/GraphMatchingSoftware_CL/base_graph.orb")
    shutil.copyfile("../Data/tracsis_tests/" + test + "/additional_graph.orb", "../Data/tracsis_tests/" + test + "/GraphMatchingSoftware_CL/additional_graph.orb")
    filenames = ["base_graph.orb", "additional_graph.orb"]
    path = "../Data/tracsis_tests/" + test + "/GraphMatchingSoftware_CL/"
    for filename in filenames:
        directory = filename.split(".")
        zfName = filename
        pre, ext = os.path.splitext(path+zfName)
        os.rename(path+zfName, pre + ".zip")
        zfName = pre + ".zip"
        with zipfile.ZipFile(zfName, 'r') as zip_ref:
            zip_ref.extractall(path + directory[0])

def create_GMSCL_tracsis():
    """Creates XML files from .orb files and places in folders in tracsis_master_tests folder
  Args:
    test (String): the directory chosen by the user
    

  Returns:
    Void: 
  """
    os.mkdir("../Data/tracsis_master_tests/GraphMatchingSoftware_CL")
    shutil.copyfile("../Data/tracsis_master_tests/inm.orb", "../Data/tracsis_master_tests/GraphMatchingSoftware_CL/inm.orb")
    shutil.copyfile("../Data/tracsis_master_tests/tps.orb", "../Data/tracsis_master_tests/GraphMatchingSoftware_CL/tps.orb")
    filenames = ["inm.orb", "tps.orb"]
    path = "../Data/tracsis_master_tests/GraphMatchingSoftware_CL/"
    for filename in filenames:
        directory = filename.split(".")
        zfName = filename
        pre, ext = os.path.splitext(path+zfName)
        os.rename(path+zfName, pre + ".zip")
        zfName = pre + ".zip"
        with zipfile.ZipFile(zfName, 'r') as zip_ref:
            zip_ref.extractall(path + directory[0])
        
