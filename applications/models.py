from django.db import models


STATUS_CHOICES = (
    ('готов к выдаче', 'Готов к выдаче'),
    ('закуп', 'Закуп'),
    ('необходимо заточить', 'Необходимо заточить'),
    ('на заточке', 'На заточке'),
    ('завершена', 'Завершена'),
)

class Applications(models.Model):
    num = models.CharField(primary_key=True, max_length=50)
    requested_equipment = models.TextField()
    avtor = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True)
    department = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return f"Дата:{self.date} Автор:{self.avtor} №:{self.num}"

    class Meta:
        managed = True
        db_table = 'Applications'