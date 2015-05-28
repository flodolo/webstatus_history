#! /usr/bin/env bash

MAIN_FOLDER=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $MAIN_FOLDER/..
# Empty cache
rm cache/*.csv

# Update repository
git pull

# Update database
./scripts/import.py
