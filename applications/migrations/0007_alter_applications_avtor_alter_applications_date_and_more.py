# Generated by Django 4.2 on 2023-09-11 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_alter_applications_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='avtor',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='department',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='status',
            field=models.CharField(blank=True, choices=[('готов к выдаче', 'Готов к выдаче'), ('закуп', 'Закуп'), ('необходимо заточить', 'Необходимо заточить'), ('на заточке', 'На заточке'), ('завершена', 'Завершена')], default='Готово к выдаче', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='user',
            field=models.CharField(max_length=100, null=True),
        ),
    ]