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
    requested_equipment = models.TextField(null=True, blank=True,)
    avtor = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True, default=None)
    department = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[2][1])

    def __str__(self):
        return f"Дата:{self.date} Автор:{self.avtor} №:{self.num}"

    class Meta:
        managed = True
        db_table = 'Applications'
