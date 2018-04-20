# C2-Framework
------------
## Full docs: https://c2f.gitbook.io/docs
## C2-SDK: https://github.com/Cgboal/C2-SDK
## Example Modules: https://github.com/Cgboal/C2F-Modules
------------

Welcome to the documentation for the Command and Control development Framework, or, C2F. This project was created as part of an Honours thesis, and thus it is not currently suitable for deployment in production environments. Consider this a Proof of Concept. With that disclaimer out of the way, let's move on.

C2F is a framework for creating applications (modules) to be ran within a C2 style network in an effort to increase the homogeneity of applications designed to be managed and run across a wide range of hosts (agents). 

The modules which can be deployed and managed by C2F come in the form of Docker containers. The use of containers allows modules to be encapsulated along with all their dependencies which enables not only more complex module functionality, but easier management and cleanup of modules. Through utilising containers, C2F allows for remote hosts to be instrumentalized to perform a variety of self-contained tasks. Unlike other container management systems such as Kubernetes, C2F focusses on running containers on independent systems, and collating their results.

C2F implements a management web interface which serves as a frontend for the API, allowing users to upload and assimilate new modules, create groups of agents, instruct groups to run modules, and finally present the results reported by agents. 
