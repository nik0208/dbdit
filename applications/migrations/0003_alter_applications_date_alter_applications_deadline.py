# Generated by Django 4.2.5 on 2023-11-03 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_alter_applications_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='deadline',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
