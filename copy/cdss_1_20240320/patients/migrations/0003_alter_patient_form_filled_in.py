# Generated by Django 5.0.1 on 2024-02-14 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_patient_form_filled_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='form_filled_in',
            field=models.BooleanField(default=False),
        ),
    ]
