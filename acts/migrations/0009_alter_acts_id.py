# Generated by Django 4.2.3 on 2023-09-15 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acts', '0008_remove_acts_user_lower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acts',
            name='id',
            field=models.AutoField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
