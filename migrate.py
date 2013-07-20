#!/usr/bin/python

import os
import sys

from pygithub3 import Github
from sh import git, cd, svn, grep

import xml.etree.ElementTree as ET

TOKEN = sys.argv[1]

sourceRoot = "~/ros/fuerte/tue/trunk"
destinationRoot = "~/ros/fuerte/tue/git"

gh = Github(token=TOKEN)

def create_repo(name, description, language='python'):
    print "Creating {2} repo {0}: {1}".format(name, description, language)
    import ipdb; ipdb.set_trace()
    repo = gh.repos.create(dict(name=name, 
                                description=description, 
                                gitignore_template=language, 
                                auto_init='true'), 
                            in_org='tue-robotics-lab')
    return repo


def migrate_repo(packagepath, destination_path, authors="/home/loy/ros/fuerte/tue/authors.txt"):
    """#The process to migrate a project is:
    # Create a new repository.
    $ git svn clone <svn_url> --no-metadata <destination_path>
    $ cd ~/ros/fuerte/tue/git/challenge_cleanup
    $ git remote add origin <repo https url>
    $ git pull origin master
    $ git push origin master"""

    svn_url = svnurl_for_path(packagepath)
    language, name, description = get_package_info(packagepath)

    repo = create_repo(name, description, language=language)
    
    #TODO: Has some issues still:
    #  STDERR:
    #    Using existing [svn-remote "svn"]
    #    svn-remote.svn.fetch already set to track :refs/remotes/git-svn
    git.svn.clone(svn_url, destination_path, no_metadata=True, A=authors)
    
    cd(destination_path)
    git.remote.add("origin", repo.clone_url)
    git.pull("origin", "master")
    git.push("origin", "master")


def scan_for_rospackages(path):
    path = os.path.expanduser(path)
    for root, dirs, files in os.walk(path):
        if "manifest.xml" in files:
            yield root

def svnurl_for_path(path):
    cd(path)
    url = grep(svn.info(), "URL: ")
    url = url.replace("URL: ", "").replace("\n", "")
    return url

def get_package_info(packagepath):
    """Check the manifest.xml to 
        * check the used language (by checking for rospy or roscpp)
        * Get the name of the package
        * Get the description"""
    manifestfile = packagepath+"/manifest.xml"
    
    tree = ET.parse(manifestfile)

    language, name, description = "", "", ""

    #Find dependencies for language
    depends = tree.findall("depend")
    dependencies = [dep.attrib["package"] for dep in depends]

    roslang2lang = {"rospy":"python", "roscpp":"c++", "roslisp":"lisp", "rosjava_jni":"java"}

    for roslang, lang in roslang2lang.iteritems():
        if roslang in dependencies:
            language = lang

    #Get language
    name = packagepath.split("/")[-1]

    #Get description
    desc = tree.findall("description")[0]
    description = desc.text.replace('\n', '').strip()

    return language, name, description

if __name__ == "__main__":
    for packagepath in scan_for_rospackages(sourceRoot):
        _, name, _ = get_package_info(packagepath)
        
        destination = os.path.join(os.path.expanduser(destinationRoot), name)
        print "Migrating {0} to {1} ...".format(packagepath, destination)
        import ipdb; ipdb.set_trace()

        migrate_repo(packagepath, destination)