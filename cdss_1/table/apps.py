from django.apps import AppConfig

class TableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'table'

    def ready(self):
        # Import the model and the management command
        from .models import Vitals_table
        from django.core.management import call_command

        # Check if there's any data in the Vitals_table
        if not Vitals_table.objects.exists():
            # Run the management command to load data
            call_command('load_vitals_data')