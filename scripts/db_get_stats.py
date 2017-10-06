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

    projects = [
        'testpilot-send',
        'testpilot-minvid',
        'testpilot-notes',
        'testpilot-tabcenter',
        'testpilot-snoozetabs',
        'testpilot-tabcenter',
        'testpilot',
        'loop-client-l10n',
        'pocket',
        'outofdate-notifications-system-addon',
        'activity-stream',
        'firefox-screenshots',
    ]
    years = ['2016', '2017']
    ref_locale = {
        'activity-stream': 'pl',
    }

    # Connect to SQLite database
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    for project in projects:
        locale = ref_locale.get(project, 'en-US')
        print('\nProject {}\n'.format(project))
        previous_total = 0
        for year in years:
            strings_removed = 0
            strings_added = 0
            cursor.execute(
                'SELECT * FROM stats WHERE project_id=? AND locale=? AND day>=? AND day<=?',
                [
                    project, locale, '{}0101'.format(year), '{}1231'.format(year)
                ]
            )
            data = cursor.fetchall()
            if not data:
                print('{}: no data available'.format(year))
                continue
            for row in data:
                if row['total'] != previous_total:
                    if row['total'] < previous_total:
                        strings_removed += previous_total - row['total']
                    elif row['total'] > previous_total:
                        strings_added += row['total'] - previous_total
                    previous_total = row['total']
            print('{}: Total: {} - Added: {} - Removed: {}'.format(year, previous_total, strings_added, strings_removed))

    # Clean up and close connection
    connection.execute('VACUUM')
    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
