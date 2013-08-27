Migration Tools
===============

$ sudo apt-get install git-core git-svn
$ git clone https://github.com/tue-robotics-lab/migration_tools.git
$ cd migration_tools
$ sudo python setup.py install #Installs sh, PyGithub and ipdb
$ ./clone_all.py <API key> https #To get all repositories from GitHub.
$ #To migrate: ./migrate.py --help

The API key is needed to ask the GitHub api to list all repositories.

Converts ROS packages in the TU/e SVN-trunk directory to GitHub repositories for the tue-robotics-lab organization.

To run, you'll need a GitHub token, which you can obtain from your account settings. 
You need to have permission to add repositories to the organization for (some of) this to work of course. 

