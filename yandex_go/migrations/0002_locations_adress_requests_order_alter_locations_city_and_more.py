# Generated by Django 4.2.3 on 2023-08-03 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_go', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='adress',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='requests',
            name='order',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='locations',
            name='city',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='locations',
            name='coordinate',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='locations',
            name='name',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='requests',
            name='destination_point',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='requests',
            name='start_point',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='requests',
            name='type',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='requests',
            name='user',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='usersya',
            name='group',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='usersya',
            name='name',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='usersya',
            name='user_id',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
