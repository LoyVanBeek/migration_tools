#!/usr/bin/python

# TODO: Be more verbose, optionally

import os
import sys
import argparse

import github
# github.enable_console_debug_logging()

from sh import git, cd, svn, grep

import xml.etree.ElementTree as ET


def create_repo(name, description, language='python'):
    print "Creating {2} repo {0}: {1}".format(name, description, language)
    # import ipdb; ipdb.set_trace()
    repo = tue.create_repo(name=name,
                           description=description,
                           gitignore_template=language,
                           auto_init=True)
    return repo


def migrate_repo(packagepath, destination_path, use_https, authors="~/ros/fuerte/tue/authors.txt"):
    """#The process to migrate a project is:
    # Create a new repository.
    $ git svn clone <svn_url> <destination_path>
    $ cd ~/ros/fuerte/tue/git/challenge_cleanup
    $ git remote add origin <repo https url>
    $ git pull origin master
    $ git push origin master"""

    authors = os.path.expanduser(authors)

    svn_url = svnurl_for_path(packagepath)
    language, name, description = get_package_info(packagepath)

    try:
        repo = create_repo(name, description, language=language)
    except github.GithubException as e:
        if e.status == 422:
            cont = raw_input(
                "The repo has an invalid field, it could already exist. Please verify and press 'c' to continue without first creating the repo: ")
            if 'c' in cont:
                repo = tue.get_repo(name)
            else:
                sys.stderr.write("Could not migrate {0}".format(name))
                return

    print "git svn clone {0} {1} A={2}".format(svn_url, destination_path, authors)
    git.svn.clone(svn_url, destination_path, A=authors)

    cd(destination_path)

    if use_https:
        git_url = repo.clone_url
    else:
        git_url = repo.ssh_url

    print "git remote add origin {0}".format(git_url)
    git.remote.add("origin", git_url)

    print "git pull origin master"
    git.pull("origin", "master")

    print "git push origin master"
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
    manifestfile = packagepath + "/manifest.xml"

    tree = ET.parse(manifestfile)

    language, name, description = "", "", ""

    # Find dependencies for language
    depends = tree.findall("depend")
    dependencies = [dep.attrib["package"] for dep in depends]

    roslang2lang = {"rospy": "python", "roscpp":
                    "c++", "roslisp": "lisp", "rosjava_jni": "java"}

    for roslang, lang in roslang2lang.iteritems():
        if roslang in dependencies:
            language = lang

    # Get language
    name = packagepath.split("/")[-1]

    # Get description
    desc = tree.findall("description")[0]
    description = desc.text.replace('\n', '').strip()

    return language, name, description


def migrate_for_path(packagepath, use_https):
    _, name, _ = get_package_info(packagepath)
    destination = os.path.join(destinationRoot, name)
    if not os.path.exists(destination):  # Only do conversion is path does not yet exist
        print "Migrating {0} to {1} ...".format(packagepath, destination)
        #import ipdb; ipdb.set_trace()
        migrate_repo(packagepath, destination, use_https)
        print "-" * 5, name, "done", "-"*5
    else: 
        print "{0} already migrated at {1}. git svn rebase-ing instead to bring up to date".format(packagepath, destination)
        git.pull("origin", "master")
        git.svn.rebase()
        git.push("origin", "master")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="A GitHub API application token")
    parser.add_argument("package", help="Which package to migrate. Or pass --all instead")
    parser.add_argument("method", help="Use https or ssh to talk to github. Defaults to https")
    args = parser.parse_args()

    TOKEN = args.token

    specific_package = None
    try:
        specific_package = args.package
    except IndexError:
        print "Specify a ROS package name, or --all"

    try:
        method = args.method
        if method == "--ssh":
            use_https = False
        elif method == "--https":
            use_https = True
    except IndexError:
        use_https = True

    sourceRoot = "~/ros/fuerte/tue/trunk"
    destinationRoot = "~/ros/fuerte/tue/git"

    destinationRoot = os.path.expanduser(destinationRoot)

    gh = github.Github(login_or_token=TOKEN)

    tue = gh.get_organization("tue-robotics-lab")

    if specific_package == "--all":
        for packagepath in scan_for_rospackages(sourceRoot):
            migrate_for_path(packagepath, use_https)
    else:
        packages = dict([(get_package_info(packagepath)[1], packagepath)
                         for packagepath in scan_for_rospackages(sourceRoot)])  # map names to paths
        migrate_for_path(packages[specific_package], use_https)
