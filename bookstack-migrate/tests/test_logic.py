"""Logic-focused unit tests to keep coverage reasonable in the monolithic module."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


class TestLogic(unittest.TestCase):
    def test_data_source_selector_scenarios(self):
        from bookstack_migrate import DataSourceSelector

        self.assertEqual(
            DataSourceSelector(db_available=True, api_available=True, prefer_api=False).get_best_source(),
            "database",
        )
        self.assertEqual(
            DataSourceSelector(db_available=True, api_available=True, prefer_api=True).get_best_source(),
            "api",
        )
        self.assertEqual(
            DataSourceSelector(db_available=False, api_available=True, prefer_api=False).get_best_source(),
            "api",
        )
        self.assertEqual(
            DataSourceSelector(db_available=True, api_available=False, prefer_api=False).get_best_source(),
            "database",
        )
        self.assertEqual(
            DataSourceSelector(db_available=False, api_available=False, prefer_api=False).get_best_source(),
            "none",
        )

    def test_large_instance_forces_database_even_if_prefer_api(self):
        from bookstack_migrate import DataSourceSelector

        sel = DataSourceSelector(db_available=True, api_available=True, prefer_api=True, large_instance=True)
        self.assertEqual(sel.get_best_source(), "database")

    def test_sql_dump_requires_docker(self):
        from bookstack_migrate import SqlDumpImporter, SqlDumpImportError

        with mock.patch("bookstack_migrate.shutil.which", return_value=None):
            imp = SqlDumpImporter(Path("/tmp/does-not-matter.sql"))
            with self.assertRaises(SqlDumpImportError):
                imp.start_and_import()

    def test_checkpoint_mark_incomplete_creates_archive(self):
        from bookstack_migrate import MigrationCheckpoint

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            output_dir = tmp_path / "export"
            output_dir.mkdir(parents=True)
            (output_dir / "dummy.txt").write_text("hello")

            checkpoint = MigrationCheckpoint(output_dir)
            checkpoint.add_page(123, "Example")

            fake_home = tmp_path / "home"
            (fake_home / "Downloads").mkdir(parents=True)

            with mock.patch("bookstack_migrate.Path.home", return_value=fake_home):
                archive = checkpoint.mark_incomplete()

            self.assertIsNotNone(archive)
            self.assertTrue(str(archive).endswith("_bookstack_migrate_incomplete.tar.gz"))
            self.assertTrue(Path(archive).exists())

    def test_justdoit_skips_venv_prompt(self):
        import bookstack_migrate

        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CI", None)
            os.environ.pop("BOOKSTACK_MIGRATE_SKIP_VENV_CHECK", None)

            with mock.patch.object(bookstack_migrate.sys, "argv", ["bookstack-migrate", "export", "--justdoit"]):
                with mock.patch.object(bookstack_migrate.sys.stdin, "isatty", return_value=True):
                    with mock.patch.object(
                        bookstack_migrate,
                        "check_venv_and_prompt",
                        side_effect=AssertionError("venv check should be skipped in --justdoit mode"),
                    ):
                        rc = bookstack_migrate.main()
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
