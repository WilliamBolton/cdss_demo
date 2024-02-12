# Generated by Django 5.0.1 on 2024-02-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_patient_similar_patients_csv_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='csv_path',
            new_name='vitals_csv_path',
        ),
        migrations.AddField(
            model_name='patient',
            name='patients_csv_path',
            field=models.CharField(default='nan', max_length=100),
        ),
    ]