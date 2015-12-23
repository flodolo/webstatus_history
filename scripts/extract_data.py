#!/usr/bin/env python

import argparse
import collections
import os
import sqlite3
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("locale", help="Locale to analyze")
    parser.add_argument("project_id", help="Project to analyze")
    args = parser.parse_args()

    if args.project_id == "all" and args.locale == "all":
        sys.exit(1)

    nested_dict = lambda: collections.defaultdict(nested_dict)
    output_data = nested_dict()

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

    # Store all available projects
    cursor.execute("SELECT * FROM projects")
    data = cursor.fetchall()
    available_projects = {}
    for row in data:
        available_projects[row["project_id"]] = row["project_name"]
    project_names = available_projects.values()
    project_names.sort()

    # Store all available dates
    if args.locale == "all":
        cursor.execute("SELECT DISTINCT day FROM stats")
    else:
        cursor.execute(
            "SELECT DISTINCT day FROM stats WHERE locale=?",
            (args.locale,)
        )
    data = cursor.fetchall()
    available_dates = []
    for row in data:
        available_dates.append(row["day"])
    available_dates.sort()

    # Store all available locales
    if args.project_id == "all":
        cursor.execute("SELECT DISTINCT locale FROM stats")
    else:
        cursor.execute(
            "SELECT DISTINCT locale FROM stats WHERE project_id=?",
            (args.project_id,)
        )
    data = cursor.fetchall()
    available_locales = []
    for row in data:
        available_locales.append(row["locale"])
    available_locales.sort()

    all_locales = False
    if args.project_id != "all" and args.locale != "all":
        # Only one project for one locale
        if args.project_id not in available_projects:
            # This project doesn"t exist, quit
            sys.exit(1)
        else:
            cursor.execute(
                "SELECT * FROM stats WHERE locale=? AND project_id=?",
                (args.locale, args.project_id)
            )
    else:
        # Note that both arguments cannot be set to "all"
        if args.project_id == "all":
            # All projects for this locale
            cursor.execute(
                "SELECT * FROM stats WHERE locale=?",
                (args.locale,)
            )
        else:
            # All locales for one project
            all_locales = True
            cursor.execute(
                "SELECT * FROM stats WHERE project_id=?",
                (args.project_id,)
            )

    data = cursor.fetchall()
    if data is not None:
        for row in data:
            project_name = available_projects[row["project_id"]]
            day = row["day"]
            locale = row["locale"]
            missing = row["missing"]
            untranslated = row["untranslated"]
            output_data[day][locale][project_name] = missing + untranslated

    if all_locales:
        csv_header = "Date,"
        csv_header += ",".join(available_locales)
        print csv_header
        for day in available_dates:
            csv_data = day + ","
            for locale in available_locales:
                project_name = available_projects[args.project_id]
                if project_name in output_data[day][locale]:
                    csv_data += str(output_data[day]
                                    [locale][project_name]) + ","
                else:
                    csv_data += "0,"
            print csv_data[:-1]
    else:
        csv_header = "Date,"
        csv_header += ",".join(project_names)
        print csv_header
        for day in available_dates:
            csv_data = day + ","
            for project in project_names:
                if project in output_data[day][args.locale]:
                    csv_data += str(output_data[day]
                                    [args.locale][project]) + ","
                else:
                    # Project didn't exist at the time for this locale
                    csv_data += "0,"
            print csv_data[:-1]


if __name__ == "__main__":
    main()
