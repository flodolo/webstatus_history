#!/usr/bin/env python

# This script can be used to merge multiple projects into one

import os
import sqlite3
import sys


def main():
    # Get absolute path of ../db from current script location (not current
    # folder)
    db_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir, "db"
        )
    )
    db_file = os.path.join(db_folder, "webstatus.db")

    # Connect to SQLite database
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    old_project_filter = "zamboni%"
    new_project_id = "zamboni"
    new_project_name = "Marketplace"

    cursor.execute("SELECT * FROM stats WHERE project_id LIKE '%s'" %
                   old_project_filter)
    data = cursor.fetchall()

    # Check if there are results from the SELECT
    if not data:
        print "There are no rows matching the specified filter"
        sys.exit(0)

    new_data = {}
    for row in data:
        locale = row["locale"]
        day = row["day"]
        if not locale in new_data:
            # New locale
            new_data[locale] = {}
        if not day in new_data[locale]:
            # New day
            new_data[locale][day] = {}
            new_data[locale][day]["day"] = day
            new_data[locale][day]["locale"] = locale
            new_data[locale][day]["project_id"] = new_project_id
            new_data[locale][day]["fuzzy"] = row["fuzzy"]
            new_data[locale][day]["identical"] = row["identical"]
            new_data[locale][day]["missing"] = row["missing"]
            new_data[locale][day]["percentage"] = 0
            new_data[locale][day]["total"] = row["total"]
            new_data[locale][day]["translated"] = row["translated"]
            new_data[locale][day]["untranslated"] = row["untranslated"]
        else:
            # Existing day, sum new values
            new_data[locale][day]["fuzzy"] += row["fuzzy"]
            new_data[locale][day]["identical"] += row["identical"]
            new_data[locale][day]["missing"] += row["missing"]
            new_data[locale][day]["total"] += row["total"]
            new_data[locale][day]["translated"] += row["translated"]
            new_data[locale][day]["untranslated"] += row["untranslated"]

    # Redetermine percentages
    for locale in new_data:
        for day in new_data[locale]:
            if new_data[locale][day]["translated"] > 0 and new_data[locale][day]["total"] > 0:
                row = new_data[locale][day]
                percentage = round(
                    100 * row["translated"] / float(row["total"]), 2)
                new_data[locale][day]["percentage"] = percentage

    # Delete rows from the stats table
    cursor.execute("DELETE FROM stats WHERE project_id LIKE '%s'" %
                   old_project_filter)
    print "Deleted rows from stats: %s" % cursor.rowcount

    # Delete the project
    cursor.execute("DELETE FROM projects WHERE project_id LIKE '%s'" %
                   old_project_filter)
    print "Deleted rows from projects: %s" % cursor.rowcount

    # Insert new rows in stats
    added_rows = 0
    for locale in new_data:
        for day in new_data[locale]:
            row = new_data[locale][day]
            cursor.execute(
                "INSERT INTO stats (day, project_id, locale, fuzzy, \
                 identical, missing, percentage, total, translated, \
                 untranslated) VALUES (:day, :project_id, :locale, :fuzzy, \
                 :identical, :missing, :percentage, :total, :translated, \
                 :untranslated)",
                row
            )
            added_rows += cursor.rowcount
    print "Inserted rows (stats): %s" % added_rows

    # Insert new row in projects
    cursor.execute(
        "INSERT INTO projects (project_id, project_name) VALUES (?, ?)",
        [new_project_id, new_project_name]
    )
    print "Inserted rows (projects): %s" % cursor.rowcount

    # Clean up and close connection
    connection.execute("VACUUM")
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
