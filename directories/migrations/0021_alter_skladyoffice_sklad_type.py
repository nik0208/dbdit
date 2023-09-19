# Generated by Django 4.2.3 on 2023-09-18 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0020_remove_skladyoffice_responsible_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skladyoffice',
            name='sklad_type',
            field=models.CharField(blank=True, choices=[('офис', 'Офис'), ('региональный склад', 'Региональный склад'), ('лц', 'ЛЦ'), ('магазин', 'Магазин'), ('пвз', 'ПВЗ')], max_length=50),
        ),
    ]