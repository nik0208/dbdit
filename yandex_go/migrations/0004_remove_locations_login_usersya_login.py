# Generated by Django 4.2.3 on 2023-08-07 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_go', '0003_locations_login_usersya_chosen_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locations',
            name='login',
        ),
        migrations.AddField(
            model_name='usersya',
            name='login',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
