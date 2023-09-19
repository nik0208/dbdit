from django.db import models
from directories.models import *


class Acts(models.Model):
    avtor = models.CharField(max_length=101)
    inv_dit = models.CharField(max_length=255, default="None")
    type = models.CharField(max_length=100)
    result = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)
    act_date = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=255)
    sklad = models.CharField(max_length=255)
    status = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Дата:{self.act_date} Автор:{self.avtor} ОС:{self.inv_dit}"

    class Meta:
        managed = True
        db_table = 'Acts'
