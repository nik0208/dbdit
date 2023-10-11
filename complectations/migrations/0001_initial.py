# Generated by Django 4.2 on 2023-10-11 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directories', '0001_initial'),
        ('acts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complectations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avtor', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('new_name_os', models.CharField(max_length=255)),
                ('tmc_qty', models.IntegerField()),
                ('prev_name_os', models.CharField(default='None', max_length=255)),
                ('doc_num', models.IntegerField(blank=True, default=1)),
                ('inv_dit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directories.it_os')),
                ('par_doc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='acts.acts')),
                ('tmc', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, to='directories.tmc')),
            ],
            options={
                'db_table': 'Complectations',
                'managed': True,
            },
        ),
    ]
