"""
Test custom Djaango management command
"""

from unittest.mock import patch
# patch is used to mock the behavior of the DB

from psycopg2 import OperationalError as Psycopg2Error
# possible connection errors that we might get connecting to DB

from django.core.management import call_command
# helps us to call the command for testing

from django.db.utils import OperationalError
# another exception that might be thrown by the db

from django.test import SimpleTestCase
# we are only checking if DB is not available and no need for migrations


# below is the command that we'll be mocking
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db is ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patch_sleep, patched_check):
        """
        Test waiting for db when getting OperationalError.
        Note: this is done by testing
        Note: 2 and 3 are choosen randomly
        """

        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)

        patched_check.assert_called_with(databases=['default'])
