#!/usr/bin/python

import os
import sys

from pygithub3 import Github
from sh import git, cd


USERNAME = ''
PASSWORD = ''  #Or use token instead
TOKEN = sys.argv[1]

gh = Github(token=TOKEN)

use_

def create_repo(name, description, language='python'):
    repo = gh.repos.create(dict(name=name, description=description, gitignore_template=language, auto_init='true'), in_org='tue-robotics-lab')
    return repo

def migrate_repo(svn_url, destination_path, authors="~/authors.txt"):
    """#The process to migrate a project is:
    # Create a new repository.
    $ git svn clone <svn_url> --no-metadata <destination_path>
    $ cd ~/ros/fuerte/tue/git/challenge_cleanup
    $ git remote add origin <repo https url>
    $ git pull origin master
    $ git push origin master"""

    name = svn_url.split("/")[-1] #Last part of the url
    repo = create_repo(name, "") #Check the manifest.xml to check for rospy or roscpp and specify language accordingly
    
    #TODO: Has some issues still:
    #  STDERR:
    #    Using existing [svn-remote "svn"]
    #    svn-remote.svn.fetch already set to track :refs/remotes/git-svn
    git.svn.clone(svn_url, destination_path, no_metadata=True, A=authors) 
    
    cd(destination_path)
    git.remote.add("origin", repo.clone_url)
    git.pull("origin", "master")
    git.push("origin", "master")