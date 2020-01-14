from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError, DEFAULT_DB_ALIAS
import time


# class Command(BaseCommand):
#     """
#     Django command to pause execution until database is available
#     https://www.mlr2d.org/modules/djangorestapi/09_command_to_wait_for_db
#     """
#
#     def handle(self, *args, **kwargs):
#         self.stdout.write('waiting for db ...')
#         db_conn = None
#         while not db_conn:
#             try:
#                 db_conn = connections['default']
#                 self.stdout.write(self.style.SUCCESS('db available'))
#             except OperationalError:
#                 self.stdout.write("Database unavailable, waiting 1 second ...")
#                 time.sleep(1)


class Command(BaseCommand):
    """
    Django command to pause execution until database is available
    https://www.mlr2d.org/modules/djangorestapi/09_command_to_wait_for_db
    https://github.com/18F/projects/blob/master/manage.py
    """

    def handle(self, *args, **kwargs):
        connection = connections[DEFAULT_DB_ALIAS]
        attempts = 0
        max_attempts = 30
        seconds_between_attempts = 5

        while True:
            try:
                connection.ensure_connection()
                break
            except OperationalError as e:
                if attempts >= max_attempts:
                    raise e
                attempts += 1
                time.sleep(seconds_between_attempts)
                print("Attempting to connect to database.")

        print("Connection to database established.")
