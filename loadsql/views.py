from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
import csv
from directories.models import *
from django.db import transaction


@login_required
def Loadsqls(request):
    return render(request, 'loadsql/loadsql.html')

def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        selected_option = request.POST.get('optionGroup', None)
        fs = FileSystemStorage(location='media/uploads')
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        file_extension = os.path.splitext(file.name)[1].lower()

        if file_extension != '.csv':
            try:
                # Чтение данных из Excel-файла
                data = pd.read_excel(file_path, engine='openpyxl')
                
                # Создание пути для нового CSV-файла
                csv_file_path = os.path.splitext(file_path)[0] + '.csv'
                
                # Сохранение данных в CSV-файл
                data.to_csv(csv_file_path, index=False)
                
                # Удаление исходного файла, если необходимо
                # os.remove(file_path)
                
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=400)
        if selected_option == 'Users':
            try:
                with transaction.atomic():
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
                        csvreader = csv.DictReader(csvfile)
                        
                        for row in csvreader:
                            Users.objects.create(
                                name=row['ФИО'],
                                department=row['Департамент'],
                                position=row['Должность'],
                                organization=row['Организация'],
                                subdivision=row['Подразделение']
                            )
                return HttpResponse("File successfully uploaded and processed.", status=200)

            except Exception as e:
                return HttpResponse(f"An error occurred while processing the file: {e}", status=400)
