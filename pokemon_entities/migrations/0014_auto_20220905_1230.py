# Generated by Django 3.1.14 on 2022-09-05 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0013_auto_20220905_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolution',
        ),
        migrations.RemoveField(
            model_name='pokemon',
            name='previous_evolution',
        ),
    ]
