# Generated by Django 4.2 on 2023-08-03 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complectations', '0002_alter_complectations_compl_os_1c_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complectations',
            name='compl_os_1c',
        ),
        migrations.RemoveField(
            model_name='complectations',
            name='spisanie_tmc_1c',
        ),
    ]
