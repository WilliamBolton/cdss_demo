# Generated by Django 5.0.1 on 2024-02-06 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vitals_plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.CharField(max_length=255)),
                ('zero', models.DecimalField(decimal_places=2, max_digits=10)),
                ('one', models.DecimalField(decimal_places=2, max_digits=10)),
                ('two', models.DecimalField(decimal_places=2, max_digits=10)),
                ('three', models.DecimalField(decimal_places=2, max_digits=10)),
                ('four', models.DecimalField(decimal_places=2, max_digits=10)),
                ('five', models.DecimalField(decimal_places=2, max_digits=10)),
                ('six', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seven', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
