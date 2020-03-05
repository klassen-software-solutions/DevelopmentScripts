#!/usr/bin/env bash

# Open a given directory in Xcode. This is intended primarily to allow an "Open in Xcode"
# custom action to be added to Sourcetree.

set -e

dir="$1"
if [ "$dir" = "" ]; then
    echo "usage: open-xcode-project.sh <directory>"
    exit 255
fi
if [ "$dir" = "." ]; then
    dir=$(pwd)
fi

proj=$(basename "$dir")
fn=$(echo "$dir/$proj.xcodeproj" | sed "s/ /\\\\ /g")
if [ -d "$fn" ]; then
    echo "Found exact match, opening $fn"
    open "$fn"
else
    count=$(find "$dir" -name '*.xcodeproj' | wc -l)
    if [ "$count" -eq 1 ]; then
        fn=$(find "$dir" -name '*.xcodeproj')
        echo "Found exactly one project, opening $fn"
        open "$fn"
    else
        if [ -f Package.swift ]; then
            echo "Found a Swift pacakge file, opening Package.swift"
            open Package.swift
        else
            echo "No project found, opening everything"
            cd "$dir"
            files=$(find . -maxdepth 1 -type f -not -path '*/\.*' -not -name '*.png' | sort)
            dirs=$(find . -maxdepth 1 -type d -not -path '*/\.*' -not -path '.' | sort)
            if [ -d .github ]; then
                dirs=".github $dirs"
            fi
            echo "$files"
            echo "$dirs"

            # shellcheck disable=SC2086
            #   Justification: None of the listed alternatives work in this instance.
            open -a Xcode $dirs $files
        fi
    fi
fi
