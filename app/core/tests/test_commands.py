from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2OperationalError
from django.core.management import call_command
from django.test import SimpleTestCase
from django.db.utils import OperationalError


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patch_check):
        """Test waiting for database if database is ready."""
        patch_check.return_value = True
        call_command('wait_for_db')
        patch_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep', return_value=None)
    def test_wait_for_db_delay(self, patch_sleep, patch_check):
        """Test waiting for database when getting errors."""
        patch_check.side_effect = (
            [Psycopg2OperationalError] * 2 + [OperationalError] * 3 + [True]
        )
        call_command('wait_for_db')
        self.assertEqual(patch_check.call_count, 6)
        patch_check.assert_called_with(databases=['default'])
