from django.db import models


# GROUP_CHOICES = (
#     ('Мини ПК ITEKS', 'Мини ПК ITEKS'),
#     ('Мониторы ITMNT', 'Мониторы ITMNT'),
#     ('Моноблок ITMNB', 'Моноблок ITMNB'),
#     ('Ноутбук ITNTB', 'Ноутбук ITNTB'),
#     ('Планшет ITPAD', 'Планшет ITPAD'),
#     ('Сервер ITSRV', 'Сервер ITSRV'),
#     ('Система хранения данных ITSHD', 'Система хранения данных ITSHD'),
#     ('Системный блок, Тонкий клиент ITWKS', 'Системный блок, Тонкий клиент ITWKS'),
#     ('Видеорегистраторы ITVDN', 'Видеорегистраторы ITVDN'),
#     ('Жесткие диски ITHDD', 'Жесткие диски ITHDD'),
#     ('ИБП (источники бесперебойного питания) Стабилизатор ITUPS',
#      'ИБП (источники бесперебойного питания) Стабилизатор ITUPS'),
#     ('Кассовое оборудование ITKSS', 'Кассовое оборудование ITKSS'),
#     ('Охранное видеонаблюдение (Видеокамеры ITVDC)',
#      'Охранное видеонаблюдение (Видеокамеры ITVDC)'),
#     ('Принтеры, МФУ, копировальные аппараты ITPRN',
#      'Принтеры, МФУ, копировальные аппараты ITPRN'),
#     ('Проектор ITPRK', 'Проектор ITPRK'),
#     ('Сетевое оборудование ITETH', 'Сетевое оборудование ITETH'),
#     ('Сканеры штрихкода ITSCN', 'Сканеры штрихкода ITSCN'),
#     ('Счетчики посетителей ITCNT', 'Счетчики посетителей ITCNT'),
#     ('Телефон, факс ITTLF', 'Телефон, факс ITTLF'),
#     ('Терминал для сбора данных ITTCD,  подставки под ТСД, зарядные устройства для ТСД',
#      'Терминал для сбора данных ITTCD,  подставки под ТСД, зарядные устройства для ТСД'),
#     ('Шкаф коммутационный, серверный  ITBOX',
#      'Шкаф коммутационный, серверный  ITBOX'),
# )

class IT_OS(models.Model):
    inv_dit = models.CharField(primary_key=True, max_length=100)
    name_os = models.CharField(max_length=255, default="None")
    inpute_date = models.DateTimeField(null=True)
    os_group = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=255, null=True, default="None")
    original_price = models.FloatField(default='100')

    def __str__(self):
        return self.name_os

    class Meta:
        managed = True
        db_table = 'IT_OS'


TYPE_CHOICES = (
    ('офис', 'Офис'),
    ('региональный склад', 'Региональный склад'),
    ('лц', 'ЛЦ'),
    ('магазин', 'Магазин'),
    ('пвз', 'ПВЗ'),
)


class SkladyOffice(models.Model):
    sklad_name = models.CharField(primary_key=True, max_length=50)
    sklad_type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, blank=True)
    sklad_city = models.CharField(max_length=50, blank=True, null=True)
    sklad_adress = models.CharField(max_length=100)
    sklad_name_lower = models.CharField(max_length=50, blank=True, null = True)

    def save(self, *args, **kwargs):
        if self.sklad_name:
            self.sklad_name_lower = self.sklad_name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sklad_name

    class Meta:
        managed = True
        db_table = 'Sklady_Office'


class Tmc(models.Model):
    tmc_name = models.CharField(max_length=50)
    tmc_article = models.CharField(max_length=50)
    web_code = models.CharField(primary_key=True, max_length=50)
    tmc_price = models.FloatField(default=100)

    def __str__(self):
        return self.tmc_name

    class Meta:
        managed = True
        db_table = 'Tmc'


class Users(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    department = models.CharField(max_length=100, null=True)
    position = models.CharField(max_length=255, null=True)
    organization = models.CharField(max_length=255, null=True)
    subdivision = models.CharField(max_length=255, null=True)
    # Дополнительное поле для имени пользователя в нижнем регистре
    name_lower = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name_lower = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'Users'


class OsGroup(models.Model):
    group_name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.group_name

    class Meta:
        managed = True
        db_table = 'OS_Group'


class Avtor(models.Model):
    avtor_name = models.CharField(primary_key=True, max_length=50)
    avtor_doljnost = models.CharField(max_length=50)
    avtor_otdel = models.CharField(max_length=50)

    def __str__(self):
        return self.avtor_name

    class Meta:
        managed = True
        db_table = 'avtor'
