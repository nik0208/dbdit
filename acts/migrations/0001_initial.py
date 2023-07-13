# Generated by Django 4.2.1 on 2023-06-15 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avtor', models.CharField(max_length=100)),
                ('act_type', models.CharField(max_length=100)),
                ('result', models.CharField(max_length=255)),
                ('conclusion', models.CharField(max_length=255)),
                ('act_date', models.DateField(auto_now_add=True)),
                ('os', models.ManyToManyField(to='directories.it_os')),
                ('sklad', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='directories.skladyoffice')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='directories.users')),
            ],
            options={
                'db_table': 'Acts',
                'managed': True,
            },
        ),
    ]
