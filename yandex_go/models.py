from django.db import models

class Requests(models.Model):
    user = models.CharField(max_length=100, default="None")
    type = models.CharField(max_length=100, default="None")
    date = models.DateTimeField()
    start_point = models.CharField(max_length=100, default="None")
    destination_point = models.CharField(max_length=100, default="None")
    receiver = models.CharField(max_length=255, null=True, default="None")
    status = models.BooleanField()
    order = models.CharField(max_length=100, default="None")

    def __str__(self):
        return f"{self.user} {self.date} {self.destination_point}"

    class Meta:
        managed = True
        db_table = 'Requests'
        
class Locations(models.Model):
    city = models.CharField(max_length=100, default="None")
    name = models.CharField(max_length=100, default="None")
    login = models.CharField(max_length=255, default="None")
    adress = models.CharField(max_length=255, default="None")
    coordinate = models.CharField(max_length=100, default="None")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'Locations'

class UsersYa(models.Model):
    name = models.CharField(max_length=100, default="None")
    phone_number = models.CharField(max_length=10)
    group = models.CharField(max_length=100, default="None")
    user_id = models.CharField(max_length=100, default="None")
    chosen_city = models.CharField(max_length=100, default="None")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        managed = True
        db_table = 'UsersYa'