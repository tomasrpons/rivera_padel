# Generated by Django 3.1.4 on 2021-01-12 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20210112_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fixedreservation',
            old_name='duration',
            new_name='fixed_duration',
        ),
        migrations.RenameField(
            model_name='fixedreservation',
            old_name='reservation_id',
            new_name='fixed_reservation_id',
        ),
        migrations.RenameField(
            model_name='fixedreservation',
            old_name='start_time',
            new_name='fixed_start_time',
        ),
    ]
