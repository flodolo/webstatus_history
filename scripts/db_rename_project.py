#!/usr/bin/env python

# This script can be used to rename a project

import argparse
import os
import sqlite3
import sys


def main():
    # Get absolute path of ../db from current script location (not current
    # folder)
    db_folder = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir, 'db'
        )
    )
    db_file = os.path.join(db_folder, 'webstatus.db')

    old_record = {
        'id': 'olympia',
        'name': 'AMO (olympia)'
    }

    new_record = {
        'id': 'addons-server',
        'name': 'AMO'
    }

    # Connect to SQLite database
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Check if the project exists
    cursor.execute('SELECT * FROM stats WHERE project_id=?', [old_record['id']])
    data = cursor.fetchall()
    if not data:
        print 'Project "{0}" is not available'.format(old_record['id'])
        sys.exit(0)

    # Update data in projects table
    cursor.execute(
        'UPDATE projects SET project_id=?, project_name=? WHERE project_id=?',
        [new_record['id'], new_record['name'], old_record['id']]
    )
    if cursor.rowcount:
        print 'Updated project_id and project_name for {0}'.format(old_record['id'])

    # Update data in stats table
    cursor.execute(
        'UPDATE stats SET project_id=? WHERE project_id=?',
        [new_record['id'], old_record['id']]
    )
    print 'Updated rows (stats):', cursor.rowcount

    # Clean up and close connection
    connection.execute('VACUUM')
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
