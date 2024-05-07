from django.core.management.base import BaseCommand
import shutil
import os

class Command(BaseCommand):
    help = 'Backs up the database file to a backup directory.'

    def handle(self, *args, **options):
        # Make sure paths are correctly defined relative to the manage.py file
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')
        backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backups', 'backup.sqlite3')
        
        # Ensure the backup directory exists
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Perform the backup
        shutil.copy2(db_path, backup_path)
        self.stdout.write(self.style.SUCCESS('Database successfully backed up'))
