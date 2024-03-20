import collections
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Reset the SQLite database and apply migrations'

    def handle(self, *args, **options):
        database_path = os.path.join('db.sqlite3')

        if os.path.exists(database_path):
            os.remove(database_path)
            self.stdout.write(self.style.SUCCESS(f'Deleted database: {database_path}'))
        
        # Reset primary key sequences
        #self.stdout.write(self.style.SUCCESS('Resetting primary key sequences...'))
        #self.reset_primary_keys()

        # Create a new migration
        self.stdout.write(self.style.SUCCESS('Creating new migration...'))
        self.call_command('makemigrations', 'patients')

        # Apply the migration
        self.stdout.write(self.style.SUCCESS('Applying migration...'))
        self.call_command('migrate', 'patients')

        self.stdout.write(self.style.SUCCESS('Database reset and migrations applied successfully'))

    def reset_primary_keys(self):
        with collections['default'].cursor() as cursor:
            cursor.execute('SELECT name FROM sqlite_sequence;')
            tables = [row[0] for row in cursor.fetchall()]
            for table in tables:
                cursor.execute(f'UPDATE {table} SET id = 1 WHERE id IS NOT NULL;')