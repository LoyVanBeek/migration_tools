#!/bin/sh
for dir in ./*; do (echo "$dir" && cd "$dir" && git pull origin master && git svn rebase && git pull origin master && git push && echo "---------"); done