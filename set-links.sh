#!/usr/bin/env bash

set -e

if [ "$#" -ne 1 ]; then
    echo "usage: set-links.sh <targetdirectory>"
    exit 255
fi

targetdirectory=$1
echo "Installing links into $targetdirectory"

cwd=$(pwd)
for fn in *.py *.sh; do
    echo -n "...$fn"
    targetlink="$targetdirectory/$fn"
    if [ -L "$targetlink" ]; then
        rm "$targetlink"
    else
        echo -n " (new)"
    fi
    echo ""
    ln -s "$cwd/$fn" "$targetdirectory"
done
