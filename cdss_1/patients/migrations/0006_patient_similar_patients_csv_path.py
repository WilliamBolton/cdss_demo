# Generated by Django 5.0.1 on 2024-02-08 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_patient_guideline_patient_prediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='similar_patients_csv_path',
            field=models.CharField(default='nan', max_length=100),
        ),
    ]