#! /usr/bin/env bash

MAIN_FOLDER=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Update repository
cd $MAIN_FOLDER/..
git pull

DAY=$(date +"%Y%m%d")
# Remove previous archive.zip, create new one and commit it
rm -f db/archive.zip
zip -j db/archive.zip db/webstatus.db
git add db/archive.zip
git commit -m "Update data ($DAY)"
git push
