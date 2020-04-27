# comp3931_indproj

##Python 

###Python environment installs 

pip install the following libraries<br/>

* networkx<br/>
* matplotlib<br/>
* random<br/>
* lxml<br/>
* pygraphviz<br/>

###Creating test data with create.py
**Instructions for use**<br/>
From the root directory of git repo navigate to /CreateTestGraphs_Py/<br/>
Run "python create.py"<br/>
Follow program instructions<br/>

note.<br/> 
some large input numbers may fail<br/>
currently unable to create graph with zero differences<br/>

##C++

###Visual Studio 2019 environment set up

GraphMatchingSoftware_CL makes use of the following Boost libraries:
* graph
* tuple
* filesystem
* property_tree
* foreach

Boost downloaded and linked to project using vcpkg package manager for C++

vcpkg download from here: https://github.com/microsoft/vcpkg<br/>
Instructions for use: https://docs.microsoft.com/en-us/cpp/build/vcpkg?view=vs-2019


###Checking graph differences with GraphMatchingSoftware_CL
**Instructions for use**<br/>
Currently runnable only from solution explorer of IDE<br/>
Build project. Run.<br/>
Follow program instructions<br/>