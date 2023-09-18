# Generated by Django 4.2 on 2023-09-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_alter_applications_avtor_alter_applications_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='avtor',
            field=models.CharField(blank=True, default='Готово к выдаче', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='deadline',
            field=models.DateField(blank=True, default='Готово к выдаче', null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='department',
            field=models.CharField(blank=True, default='Готово к выдаче', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='requested_equipment',
            field=models.TextField(blank=True, default='Готово к выдаче', null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='user',
            field=models.CharField(blank=True, default='Готово к выдаче', max_length=100, null=True),
        ),
    ]