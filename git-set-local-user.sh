#!/bin/bash

# This script starts in the current directory and recursively sets the local
# configuration for user.name and user.email to the arguments given on the command
# line. This is useful if you have a directory of git projects for which you wish
# to have name and email settings that differ from your global ones.
#
# Note that for this to work, you need to run the script each time you clone or
# create a new repository within the directory space.

if [ $# -ne 2 ]; then
    echo "usage: git-set-local-user.sh <name> <email>"
    exit 255
fi

name=$1
email=$2
cwd=$(pwd)
find . -type d | while read -r dir; do
    if [ -d "$dir/.git" ]; then
        echo "...in $dir"
        cd "$dir" || exit 255
        git config --local --unset-all user.name
        git config --local --unset-all user.email
        git config --local --add user.name "$name"
        git config --local --add user.email "$email"
        cd "$cwd" || exit 255
    fi
done
