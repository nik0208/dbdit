import csv
from directories.models import Users

with open('mydata.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        Users.objects.create(name=row['ФИО'],
                             department=row['Департамент'],
                             position = row['Должность '],
                             organization=row['Организация'],
                             subdivision=row['Подразделение'])

