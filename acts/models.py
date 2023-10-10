from django.db import models
from directories.models import *


class Acts(models.Model):
    avtor = models.CharField(max_length=101)
    inv_dit = models.ForeignKey(
        IT_OS, on_delete=models.PROTECT, null=True, blank=True)
    type = models.CharField(max_length=100)
    result = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)
    act_date = models.DateField(auto_now_add=True)
    new_user = models.ForeignKey(
        Users, on_delete=models.PROTECT, null=True, blank=True)
    new_sklad = models.ForeignKey(
        SkladyOffice, on_delete=models.PROTECT, null=True, blank=True)
    user = models.CharField(max_length=255, null=True, blank=True)
    sklad = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Дата:{self.act_date} Автор:{self.avtor} ОС:{self.inv_dit}"

    class Meta:
        managed = True
        db_table = 'Acts'
