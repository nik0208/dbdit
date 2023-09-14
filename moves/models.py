from django.db import models
from directories.models import *
from acts.models import *


class Move(models.Model):
    move_num = models.CharField(max_length=20, null=True)
    move_date = models.DateField(null=True)
    status = models.CharField(max_length=100, null=True)
    avtor = models.CharField(max_length=100)
    sklad = models.CharField(max_length=100)
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True)
    par_dok = models.ForeignKey(
        Acts, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.move_date} {self.user} {self.sklad}"

    class Meta:
        abstract = True


class OsMove(Move):
    equipment = models.ForeignKey(
        IT_OS, on_delete=models.PROTECT, default=None)

    class Meta:
        managed = True
        db_table = 'OS_move'


class TmcMove(Move):
    equipment = models.CharField(max_length=100)
    qty = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'TMC_move'
