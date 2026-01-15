# BookStack Migration Tool (Python-only)

Single-file Python 3 script to export BookStack content to DokuWiki format.

## Requirements
- Python 3.8+ (standard library only for API mode)
- Optional DB drivers for database exports:
  - `mysql-connector-python` or `mariadb`
- Optional Docker for `--sql-file` imports

## Quick Start
1) Set API credentials (from BookStack admin panel):
   ```bash
   export BOOKSTACK_BASE_URL="https://bookstack.example.com"
   export BOOKSTACK_TOKEN_ID="your_api_token_id"
   export BOOKSTACK_TOKEN_SECRET="your_api_token_secret"
   ```

2) Export via API (recommended):
   ```bash
   python3 bookstack_migrate.py export --output ./dokuwiki_export
   ```

## Database export (optional)
```bash
python3 bookstack_migrate.py export \
  --db bookstack \
  --user db_user \
  --password db_pass \
  --host localhost \
  --port 3306 \
  --output ./dokuwiki_export
```

## SQL dump import (optional, requires Docker)
```bash
python3 bookstack_migrate.py export \
  --sql-file ./bookstack.sql \
  --sql-db bookstack \
  --output ./dokuwiki_export
```

## Notes
- Logs are written to `bookstack_migrate.log` in the current directory.
- Use `--justdoit` to skip venv warnings for automated runs.
- Output layout:
  - Pages: `OUTPUT/pages/...`
  - Media: `OUTPUT/media/...`

## Windows usage
Use the Python launcher if `python3` is not available:
```powershell
py -3 bookstack_migrate.py export --output .\dokuwiki_export
```

## Full backup helper (datadir → dump + export)
If you already have a MySQL/MariaDB datadir (with `ibdata1`), you can spin up a temporary MariaDB container, create a logical dump, optionally archive BookStack instance files, and run the DokuWiki export in one step:
```powershell
py -3 bookstack_migrate.py backup `
  --datadir "C:\path\to\mysql" `           # points at the datadir containing ibdata1
  --root-user root `
  --root-password pass1234 `              # empty is allowed; set if needed
  --db bookstack `
  --host-port 3307 `                      # exposed port for the temp container
  --dump-path "C:\path\to\bookstack.backup.sql" `
  --export-output "C:\path\to\dokuwiki_export" `
  --include-files `                       # also archive .env/uploads/themes
  --files-archive "C:\path\to\bookstack-files-backup.tar.gz" `
  --instance-root "C:\path\to\BookStack"
```
Flags:
- `--skip-export` or `--skip-dump` to run only part of the workflow.
- `--image` / `--container-name` to override the MariaDB image or container name.
- If `--datadir` is not provided, the script will try to auto-detect a datadir containing `ibdata1` in common locations (current dir, parent, script dir, and `~/Downloads/mysql`).
