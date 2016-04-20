#! /usr/bin/env bash

MAIN_FOLDER=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $MAIN_FOLDER/..
# Empty cache
echo "---------------------"
echo "Clean up cache folder"
rm -f web/cache/*.csv

# Update repository
echo "Update Git repository"
git pull

# Update database
echo "Import data"
./scripts/import.py
