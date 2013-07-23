#!/usr/bin/python

import os
import sys

from github import Github
from sh import git, cd, svn, grep

import xml.etree.ElementTree as ET

TOKEN = sys.argv[1]

sourceRoot = "~/ros/fuerte/tue/trunk"
destinationRoot = "~/ros/fuerte/tue/git"

sourceRoot = os.path.expanduser(sourceRoot)
destinationRoot = os.path.expanduser(destinationRoot)

g = Github(login_or_token=TOKEN)

def clone_all_tue_packages():
	cd(destinationRoot)

	tue = g.get_organization("tue-robotics-lab")

	tue_repos = tue.get_repos()

	for repo in tue_repos:
		try:
			git.clone(repo.clone_url)
		except Exception as e:
			cd(repo.name)
			git.pull()

if __name__ == "__main__":
	clone_all_tue_packages()