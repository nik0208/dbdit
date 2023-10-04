from django.db import models

class loadsqls(models.Model):
    option = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)