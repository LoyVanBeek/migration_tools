#!/usr/bin/python

import os
import sys

from github import Github

import sh
from sh import git, cd, svn, grep

import xml.etree.ElementTree as ET

sourceRoot = "~/ros/fuerte/tue/trunk"
destinationRoot = "~/ros/fuerte/tue/git"

sourceRoot = os.path.expanduser(sourceRoot)
destinationRoot = os.path.expanduser(destinationRoot)



def clone_all_tue_packages(use_https):
    cd(destinationRoot)

    tue = g.get_organization("tue-robotics-lab")

    tue_repos = tue.get_repos()

    for repo in tue_repos:
        if use_https:
            git_url = repo.clone_url
        else:
            git_url = repo.ssh_url

        try:
            git.clone(git_url)
        except sh.ErrorReturnCode_128 as e:  # When the dir to clone already exists and is not empty, git pull this dir
            cd(repo.name)
            git.pull("origin", "master")

if __name__ == "__main__":
    TOKEN = sys.argv[1]
    g = Github(login_or_token=TOKEN)


    try:
        method = sys.argv[2]
        if method == "--ssh":
            use_https = False
        elif method == "--https":
            use_https = True
    except IndexError:
        use_https = True


    clone_all_tue_packages(use_https)
