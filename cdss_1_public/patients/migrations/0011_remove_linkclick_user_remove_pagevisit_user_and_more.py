# Generated by Django 5.0.1 on 2024-03-21 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_patient_demo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkclick',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pagevisit',
            name='user',
        ),
        migrations.DeleteModel(
            name='HoverEvent',
        ),
        migrations.DeleteModel(
            name='LinkClick',
        ),
        migrations.DeleteModel(
            name='PageVisit',
        ),
    ]
