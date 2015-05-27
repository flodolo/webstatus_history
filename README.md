# Web Status History

Add History capabilities to [Web Status](https://github.com/mozilla-l10n/webstatus).

## Getting started

### Create a database
Script expects a SQLite database in `db/webstatus.db`. You can either create one by running from the `db` folder.

```
sqlite3 webstatus.db < table_initialize.sql
```

Or copy `archive.db` as `webstatus.db`.

### Updating data
Set up a cron-job running ´scripts/import.py´.
