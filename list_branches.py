#!/usr/bin/python

# TODO: Be more verbose, optionally

import os
import sys
import argparse

from sh import git, cd, svn, grep, sed

def get_immediate_subdirectories(dir):
    return (name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name)))

def list_branches(package, ignore):
        for name in get_immediate_subdirectories("."):
            if name in packages:
                cd(name)
                branches = sed(git.branch(), r="s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
                branches = [str(branch.strip()) for branch in branches]
                active = [branch for branch in branches if branch[0] == '*'][0]
                active = active.strip("* ")
                if not active in ignore:
                    print "{2}: {0} {1}".format(active, branches, name)
                cd("..")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest="subparser_name")
    
    _list = subparsers.add_parser('list', help='list which branch subdirs are on', prog="list")
    _list.add_argument("--packages", nargs='*', help="Which package to get the branch from. Defaults to all", default="all")
    _list.add_argument("--ignore", help="Ignore (a) certain branch(es). Defaults to master", default=["master"])

    switch = subparsers.add_parser('switch', help="switch subdirectories to a given branch")
    switch.add_argument("--packages", nargs='*', help="Which packages to switch. Defaults to None", default=None)
    switch.add_argument("--branch", help="Switch the packages to the specified branch. Defaults to master", default="master")
    
    args = parser.parse_args()

    print args

    if args.subparser_name == "list":
        packages = args.packages
        if isinstance(packages, str):
            packages = [packages]
        list_branches(package=packages, ignore=args.ignore)
    if args.subparser_name == "switch":
        switch_branches(packages=args.packages, branch=args.branch)
