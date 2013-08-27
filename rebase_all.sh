#!/bin/sh
for dir in ./*; do (cd "$dir" && git pull origin master && git svn rebase && git pull origin master && git push); done