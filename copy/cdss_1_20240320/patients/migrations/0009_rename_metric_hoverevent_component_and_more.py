# Generated by Django 5.0.1 on 2024-02-16 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0008_hoverevent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hoverevent',
            old_name='metric',
            new_name='component',
        ),
        migrations.RemoveField(
            model_name='hoverevent',
            name='time',
        ),
    ]
