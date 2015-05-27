#! /usr/bin/env bash

MAIN_FOLDER=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Update repository
cd $MAIN_FOLDER/..
git pull

# Update database
./scripts/import.py
