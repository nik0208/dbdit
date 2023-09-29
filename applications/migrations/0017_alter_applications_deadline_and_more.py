# Generated by Django 4.2 on 2023-09-21 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0016_alter_applications_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='deadline',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='status',
            field=models.CharField(blank=True, choices=[('готов к выдаче', 'Готов к выдаче'), ('закуп', 'Закуп'), ('необходимо заточить', 'Необходимо заточить'), ('на заточке', 'На заточке'), ('завершена', 'Завершена')], max_length=100, null=True),
        ),
    ]