from django.db import models
from directories.models import *


class Move(models.Model):
    move_num = models.CharField(max_length=20, null=True)
    move_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default='True')
    avtor = models.CharField(max_length=100)
    sklad = models.ForeignKey(
        SkladyOffice, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.move_date} {self.user} {self.sklad}"

    class Meta:
        abstract = True


class OsMove(Move):
    equipment_os = models.ForeignKey(IT_OS, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'OS_move'


class TmcMove(Move):
    equipment_tmc = models.ForeignKey(Tmc, on_delete=models.PROTECT)
    qty = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'TMC_move'
