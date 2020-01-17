#!/usr/bin/env bash

# Recursively apply a git command and its arguments to all git repositories found
# beneath the current directory.

set -e

cwd=$(pwd)
echo "Recursively applying '$*' in $cwd..."
find . -type d | while read -r dir; do
    if [ -d "$dir/.git" ]; then
        echo "...in $dir"
        cd "$dir"
        git "$@"
        echo
        cd "$cwd"
    fi
done
