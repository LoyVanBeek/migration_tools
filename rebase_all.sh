#!/bin/sh
for dir in ./*; do (cd "$dir" && git svn rebase && git pull origin master && git push); done