# Generated by Django 4.2 on 2023-08-03 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0006_remove_users_dad_name_remove_users_last_name_and_more'),
        ('acts', '0002_rename_act_type_acts_type_remove_acts_os_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='acts',
            name='other_tech',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='acts',
            name='status',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='acts',
            name='inv_dit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directories.it_os'),
        ),
    ]
