# Generated by Django 4.2 on 2023-09-13 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moves', '0008_alter_osmove_status_alter_tmcmove_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='osmove',
            old_name='equipment_os',
            new_name='equipment',
        ),
        migrations.RenameField(
            model_name='tmcmove',
            old_name='equipment_tmc',
            new_name='equipment',
        ),
    ]