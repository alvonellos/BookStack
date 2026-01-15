# BookStack Migration Tool

Simple, single-file Python migration tool to export BookStack content to DokuWiki format.

## Overview

This repository contains a clean, consolidated migration solution in `bookstack-migrate/bookstack_migrate.py` - a single Python script with no external dependencies (for API mode).

## Quick Start

### 1. Export via API (Recommended)

Set your BookStack API credentials:

```bash
export BOOKSTACK_BASE_URL="https://bookstack.example.com"
export BOOKSTACK_TOKEN_ID="your_api_token_id"
export BOOKSTACK_TOKEN_SECRET="your_api_token_secret"
```

Run the export:

```bash
python3 bookstack-migrate/bookstack_migrate.py export --output ./dokuwiki_export
```

### 2. Export via Database (Optional)

If you have direct database access:

```bash
python3 bookstack-migrate/bookstack_migrate.py export \
  --db bookstack \
  --user db_user \
  --password db_pass \
  --host localhost \
  --port 3306 \
  --output ./dokuwiki_export
```

### 3. Full Backup Mode

If you have a MySQL/MariaDB datadir (with `ibdata1`):

```bash
python3 bookstack-migrate/bookstack_migrate.py backup \
  --datadir /path/to/mysql \
  --root-user root \
  --root-password yourpassword \
  --db bookstack \
  --host-port 3307 \
  --dump-path ./bookstack.backup.sql \
  --export-output ./dokuwiki_export
```

## Features

- **Single Python file** - No complex build systems or multiple tools
- **Zero dependencies for API mode** - Uses Python standard library
- **Multiple data sources** - API, direct DB, or SQL dump
- **Docker integration** - Optional Docker for SQL dump imports
- **Comprehensive logging** - Logs written to `bookstack_migrate.log`
- **Progress tracking** - Checkpoint system for resuming interrupted exports

## Requirements

- **Python 3.8+** (standard library only for API mode)
- **Optional**: `mysql-connector-python` or `mariadb` for database exports
- **Optional**: Docker for SQL file imports

## Output Structure

```
dokuwiki_export/
├── pages/          # Exported pages in DokuWiki format
└── media/          # Media files
```

## Documentation

See [`bookstack-migrate/README.md`](bookstack-migrate/README.md) for detailed usage and options.

## What Happened to the Complex Tooling?

Previous versions had multiple tools (Perl, Java, C, PHP, Rust) and complex shell scripts. 
This has been **consolidated into one simple Python script** for easier maintenance and usage.

## Migration Path

If you were using the old `bookstack-migration/` directory with multiple tools:
- All functionality is now in `bookstack-migrate/bookstack_migrate.py`
- The new script is simpler, cleaner, and easier to use
- No complex dependencies or build steps required

## License

See [LICENSE](LICENSE) for details.
