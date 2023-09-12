# Generated by Django 4.2 on 2023-09-11 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_alter_applications_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='status',
            field=models.CharField(blank=True, choices=[('готов к выдаче', 'Готов к выдаче'), ('закуп', 'Закуп'), ('необходимо заточить', 'Необходимо заточить'), ('на заточке', 'На заточке'), ('завершена', 'Завершена')], default='Готово к выдаче', max_length=100),
        ),
    ]
