# Generated by Django 4.2.2 on 2023-07-11 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0004_alter_it_os_inpute_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='it_os',
            name='original_price',
            field=models.FloatField(default='100'),
        ),
    ]
