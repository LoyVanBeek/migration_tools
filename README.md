Migration Tools
===============

Migration tools for the ROS packages in the TU/e SVN-trunk directory. 
Tools can move thse to GitHub repositories and help clone/git-svn rebase them all.

Installation
------------

    $ sudo apt-get install git-core git-svn
    $ git clone https://github.com/tue-robotics-lab/migration_tools.git
    $ cd migration_tools
    $ sudo python setup.py install #Installs sh, PyGithub and ipdb
    $ ./clone_all.py <API key> https #To get all repositories from GitHub.
    $ #To migrate: ./migrate.py --help

The API key is needed to ask the GitHub api to list all repositories.
You can obtain one from your account settings. 
When migrating from svn to git, you need to have permission to add repositories to the organization for this to work of course. 

