# Generated by Django 3.1.4 on 2021-01-12 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20210112_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fixedreservation',
            old_name='fixed_customer',
            new_name='customer',
        ),
    ]