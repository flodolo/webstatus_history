#!/usr/bin/env python

# This script can be used to merge multiple projects into one

import argparse
import os
import sqlite3
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_id", help="Project to remove")
    args = parser.parse_args()

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

    # Check if the project exists
    cursor.execute("SELECT * FROM stats WHERE project_id=?", [args.project_id])
    data=cursor.fetchall()
    if not data:
        print "Project '%s' is not available" % args.project_id
        sys.exit(0)

    # Delete rows from the stats table
    cursor.execute("DELETE FROM stats WHERE project_id=?", [args.project_id])
    print "Deleted rows from stats: %s" % cursor.rowcount

    # Delete the project
    cursor.execute("DELETE FROM projects WHERE project_id=?", [args.project_id])
    print "Deleted rows from projects: %s" % cursor.rowcount

    # Clean up and close connection
    connection.execute("VACUUM")
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
