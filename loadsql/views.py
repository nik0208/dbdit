from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
import csv
from directories.models import *
from acts.models import *
from django.db import transaction
import openpyxl


@login_required
def Loadsqls(request):
    return render(request, 'loadsql/loadsql.html')


def upload_file(request):
    if request.method == 'POST':

        # Проверка на наличие файла в запросе
        if 'file' not in request.FILES:
            return HttpResponse("No file found in request", status=400)

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
                data.to_csv(csv_file_path, index=False, encoding='utf-8')

                # Удаление исходного файла, если необходимо
                os.remove(file_path)

                file_path = csv_file_path

            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=400)
        if selected_option == 'Users':

            with transaction.atomic():
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
                    csvreader = csv.DictReader(csvfile)

                    for row in csvreader:
                        Users.objects.update_or_create(
                            name=row['ФИО'],
                            department=row['Департамент'],
                            position=row['Должность'],
                            organization=row['Организация'],
                            subdivision=row['Подразделение']
                        )
            os.remove(file_path)
            return redirect('/')

        elif selected_option == 'SkladyOffice':

            with transaction.atomic():
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.DictReader(csvfile)

                    for row in csvreader:
                        print(f"как бы: {row}")
                        SkladyOffice.objects.update_or_create(
                            sklad_name=row['Имя'],
                            sklad_type=row['Тип'],
                            sklad_city=row['Город'],
                            sklad_adress=row['Адрес'],
                        )
            os.remove(file_path)
            return redirect('/')

        elif selected_option == 'Tmc':

            with transaction.atomic():
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.DictReader(csvfile)

                    for row in csvreader:
                        Tmc.objects.update_or_create(
                            tmc_name=row['Номенклатура'],
                            tmc_article=row['Артикул'],
                            web_code=row['Web code'],
                            tmc_price=row['Себестоимость'],
                        )
            os.remove(file_path)
            return redirect('/directories/tmc')

        return redirect('/loadsql')
