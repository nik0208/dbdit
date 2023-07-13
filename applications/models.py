from django.db import models


STATUS_CHOICES = (
    ('готов к выдаче', 'Готов к выдаче'),
    ('закуп', 'Закуп'),
    ('на заточке', 'На заточке'),
)

class Applications(models.Model):
    num = models.CharField(max_length=50)
    requested_equipment = models.TextField()
    avtor = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True)
    department = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)