#!/usr/bin/env bash

# Shell implementation of a "watch" - like command.
# Adapted from a code found at https://stackoverflow.com/questions/9574089/os-x-bash-watch-command

set -e

if [ "$#" -eq 1 ]; then
    command=$1
    duration=2
elif [ "$#" -eq 2 ]; then
    command=$1
    duration=$2
else
    echo "usage: watch.sh <command> <sleep duration>"
    exit 1
fi

while :; do
    clear
    date
    $command
    sleep $duration
done
