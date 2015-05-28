#!/usr/bin/env python

import json
import os
import sqlite3
import urllib2
from datetime import datetime


def main():
    # Get absolute path of ../db from current script location (not current
    # folder)
    db_folder = os.path.abspath(
                        os.path.join(
                            os.path.dirname( __file__ ),
                            os.pardir, "db"
                        )
                    )
    db_file = os.path.join(db_folder, "webstatus.db")

    json_url = "https://l10n.mozilla-community.org/~flod/webstatus/web_status.json"
    try:
        response = urllib2.urlopen(json_url)
        json_data = json.load(response)
    except Exception as e:
        print "Error reading JSON data from " + json_url
        print e

    last_update = datetime.strptime(
                        json_data["metadata"]["creation_date"],
                        "%Y-%m-%d %H:%M %Z"
                    )
    day_string = last_update.strftime("%Y%m%d")
    print "Analyzing %s" % day_string

    # Connect to SQLite database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Check if we already have data for this day
    cursor.execute(
        "SELECT ID FROM stats WHERE day=?",
        (day_string,)
    )
    data = cursor.fetchone()

    imported_records = 0
    if data is None:
        # Import data
        for locale in json_data["locales"]:
            for project_id in json_data["locales"][locale]:
                current_project = json_data["locales"][locale][project_id]
                data_record = (
                    day_string,
                    project_id,
                    locale,
                    current_project["fuzzy"],
                    current_project["identical"],
                    current_project["missing"],
                    current_project["percentage"],
                    current_project["total"],
                    current_project["translated"],
                    current_project["untranslated"],
                );

                cursor.execute(
                    "INSERT INTO stats (day, project_id, locale, fuzzy, \
                     identical, missing, percentage, total, translated, \
                     untranslated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    data_record
                )
                imported_records += 1
    else:
        print "WARNING: Data already available for this day in the database"

    # Store or update projects data
    added_projects = 0
    updated_projects = 0
    for project_id in json_data["metadata"]["products"]:
        current_project = json_data["metadata"]["products"][project_id]
        cursor.execute(
            "SELECT project_name FROM projects WHERE project_id=?",
            (project_id,)
        )
        data = cursor.fetchone()
        if data is None:
            # Add missing project
            cursor.execute(
                "INSERT INTO projects (project_id, project_name) VALUES (?, ?)",
                (project_id, current_project["name"])
            )
            added_projects += 1
        else:
            # Update name of an existing project
            if data[0] != current_project["name"]:
                print data[0]
                cursor.execute(
                    "UPDATE projects SET project_name=? WHERE project_id=?",
                    (current_project["name"], project_id)
                )
                updated_projects += 1

    connection.commit()
    connection.close()

    # Output info on the process
    print "Imported records: %s" % imported_records
    print "Added projects: %s" % added_projects
    print "Updated projects: %s" % updated_projects


if __name__ == "__main__":
    main()
