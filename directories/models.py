from django.db import models

class IT_OS(models.Model):
    inv_dit = models.CharField(primary_key=True, max_length=100)
    name_os = models.CharField(max_length=100)
    inpute_date = models.DateTimeField( null=True)
    os_group = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=255, null=True, default="None")
    original_price = models.FloatField(default='100')
    

    def __str__(self):
        return f"{self.name_os} {self.inv_dit}"

    class Meta:
        managed = True
        db_table = 'IT_OS'



class SkladyOffice(models.Model):
    sklad_name = models.CharField(primary_key=True, max_length=50)
    sklad_type = models.CharField(max_length=50)
    sklad_city = models.CharField(max_length=50, blank=True, null=True)
    sklad_adress = models.CharField(max_length=100)
    responsible_person = models.ForeignKey("Users", on_delete=models.PROTECT, blank=True, null=True)

    
    def __str__(self):
        return self.sklad_name
    
    class Meta:
        managed = True
        db_table = 'Sklady_Office'


class Tmc(models.Model):
    tmc_name = models.CharField(primary_key=True, max_length=50)
    tmc_article = models.CharField(max_length=50)
    web_code = models.CharField(max_length=50)
    tmc_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.tmc_name
    
    class Meta:
        managed = True
        db_table = 'Tmc'


class Users(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    last_name = models.CharField(max_length=50)
    dad_name = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.last_name} {self.dad_name}"
    
    class Meta:
        managed = True
        db_table = 'Users'
        
        
class OsGroup(models.Model):
    group_name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.group_name
    
    class Meta:
        managed = True
        db_table = 'OS_Group'

class Avtor(models.Model):
    avtor_name = models.CharField(primary_key=True, max_length=50)
    avtor_doljnost = models.CharField(max_length=50)
    avtor_otdel = models.CharField(max_length=50)

    def __str__(self):
        return self.avtor_name
    
    class Meta:
        managed = True
        db_table = 'avtor'
