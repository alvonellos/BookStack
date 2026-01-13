"""Tests for API/config pieces in the consolidated module."""
import os
import unittest
from unittest import mock

from bookstack_migrate import BookStackError, PageRef, read_env_config


class TestApi(unittest.TestCase):
    def test_page_ref(self):
        page = PageRef(id=1, name="Test", slug="test")
        self.assertEqual(page.id, 1)
        self.assertEqual(page.name, "Test")
        self.assertEqual(page.slug, "test")
        self.assertIsNone(page.book_id)

    def test_bookstack_error(self):
        err = BookStackError("Test error", status=404)
        self.assertEqual(str(err), "Test error (status=404)")

    def test_env_config_missing_token(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("BOOKSTACK_TOKEN_ID", None)
            os.environ.pop("BOOKSTACK_TOKEN_SECRET", None)
            os.environ.pop("BOOKSTACK_API_TOKEN_ID", None)
            os.environ.pop("BOOKSTACK_API_TOKEN_SECRET", None)

            with self.assertRaises(ValueError):
                read_env_config()


if __name__ == "__main__":
    unittest.main()
