"""Tests for bookstack_migrate CLI."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = (Path(__file__).resolve().parents[1] / "bookstack_migrate.py").resolve()
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class TestCLI(unittest.TestCase):
    def test_help(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("BookStack → DokuWiki", result.stdout)

    def test_version(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "version"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("1.0.0", result.stdout)

    def test_detect_no_dokuwiki(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "detect"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("No DokuWiki", result.stdout)

    def test_export_missing_args(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "export"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertTrue("No data source" in result.stdout or "No data source" in result.stderr)

    def test_checkpoint_creation(self):
        from bookstack_migrate import MigrationCheckpoint

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            checkpoint = MigrationCheckpoint(output_dir)

            self.assertEqual(checkpoint.data["pages"], [])
            self.assertIn("start_time", checkpoint.data)

            checkpoint.add_page(1, "Test Page")
            self.assertEqual(len(checkpoint.data["pages"]), 1)
            self.assertEqual(checkpoint.data["pages"][0]["id"], 1)

            self.assertTrue((output_dir / ".migration_checkpoint.json").exists())

            checkpoint2 = MigrationCheckpoint(output_dir)
            self.assertEqual(len(checkpoint2.data["pages"]), 1)
            self.assertEqual(checkpoint2.data["pages"][0]["name"], "Test Page")


if __name__ == "__main__":
    unittest.main()
