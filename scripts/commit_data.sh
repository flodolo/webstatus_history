#! /usr/bin/env bash

MAIN_FOLDER=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Update repository
cd $MAIN_FOLDER/..
git pull

DAY=$(date +"%Y%m%d")
cp db/webstatus.db db/archive.db
git add db/archive.db
git commit -m "Update data ($DAY)"
git push
