# Generated by Django 4.2 on 2023-10-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='it_os',
            name='name_os',
            field=models.CharField(blank=True, default='None', max_length=255),
        ),
    ]