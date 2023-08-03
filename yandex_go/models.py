from django.db import models

# Create your models here.
class Requests(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    date = models.DateTimeField()
    start_point = models.CharField(max_length=100)
    destination_point = models.CharField(max_length=100)
    receiver = models.CharField(max_length=255, null=True, default="None")
    status = models.BooleanField()

    def __str__(self):
        return f"{self.user} {self.date} {self.destination_point}"

    class Meta:
        managed = True
        db_table = 'Requests'
        
class Locations(models.Model):
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    coordinate = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'Locations'

class UsersYa(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    group = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'UsersYa'