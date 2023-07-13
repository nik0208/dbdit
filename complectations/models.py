from django.db import models
from acts.models import *
from directories.models import *
#from заявки import *


class Complectations(models.Model):
    avtor = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    par_doc = models.ForeignKey(Acts, on_delete=models.PROTECT, blank=True, null=True)
    inv_dit = models.ForeignKey(IT_OS, on_delete = models.PROTECT)
    new_name_os = models.CharField(max_length=255)
    tmc = models.ManyToManyField(Tmc, blank=True)
    tmc_qty = models.IntegerField()
    spisanie_tmc_1c = models.CharField(max_length=12, blank=True, null=True)
    compl_os_1c = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.date} {self.inv_dit}"
    
    class Meta:
        managed = True
        db_table = 'Complectations'