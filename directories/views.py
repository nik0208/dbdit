from django.contrib.auth.decorators import login_required
from acts import forms
from . import models
from django.apps import apps
from openpyxl import load_workbook
from django.http import JsonResponse
from django.http import HttpResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
import os
from django.conf import settings
import subprocess
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from docxtpl import DocxTemplate
import pandas as pd
import requests
import json
import openpyxl


def upload_data_os(request, table_name='IT_OS'):

    def import_csv_to_sqlite(csv_file_path, db_name, table_name):
        # Команда для выполнения импорта CSV в SQLite
        command = f'sqlite3 "{db_name}" ".mode csv" ".import {csv_file_path} {table_name}"'

        # Запуск команды в терминале
        subprocess.run(command, shell=True)

    if request.method == 'POST':
        file = request.FILES['file']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension != '.csv':

            wb = openpyxl.load_workbook(file)
            sheet = wb.active  # Выбираем активный лист
            sheet.delete_rows(1, amount=1)
            
            # Проходимся по строкам и меняем значения в третьем столбце
            for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=3):
                first_column_value = row[0].value
                if first_column_value is not None:
                    first_five_chars = first_column_value[:5]
                    if first_five_chars == "ITEKS":
                        row[2].value = "Мини ПК ITEKS"
                    elif first_five_chars == "ITMNT":
                        row[2].value = "Мониторы ITMNT"
                    elif first_five_chars == "ITMNB":
                        row[2].value = "Моноблок ITMNB"
                    elif first_five_chars == "ITNTB":
                        row[2].value = "Ноутбук ITNTB"
                    elif first_five_chars == "ITPAD":
                        row[2].value = "Планшет ITPAD"
                    elif first_five_chars == "ITSRV":
                        row[2].value = "Сервер ITSRV"
                    elif first_five_chars == "ITSHD":
                        row[2].value = "Система хранения данных ITSHD"
                    elif first_five_chars == "ITWKS":
                        row[2].value = "Системный блок, Тонкий клиент ITWKS"
                    elif first_five_chars == "ITVDN":
                        row[2].value = "Видеорегистраторы ITVDN"
                    elif first_five_chars == "ITHDD":
                        row[2].value = "Жесткие диски ITHDD"
                    elif first_five_chars == "ITUPS":
                        row[2].value = "ИБП (источники бесперебойного питания) Стабилизатор ITUPS"
                    elif first_five_chars == "ITKSS":
                        row[2].value = "Кассовое оборудование ITKSS"
                    elif first_five_chars == "ITSAN":
                        row[2].value = "Оптические коммутаторы ITSAN"
                    elif first_five_chars == "ITVDC":
                        row[2].value = "Охранное видеонаблюдение (Видеокамеры ITVDC)"
                    elif first_five_chars == "ITPRN":
                        row[2].value = "Принтеры, МФУ, копировальные аппараты ITPRN"
                    elif first_five_chars == "ITPRK":
                        row[2].value = "Проектор ITPRK"
                    elif first_five_chars == "ITETH" or first_five_chars == "ITCSC":
                        row[2].value = "Сетевое оборудование ITETH"
                    elif first_five_chars == "ITSCN":
                        row[2].value = "Сканеры штрихкода ITSCN"
                    elif first_five_chars == "ITCNT" or first_five_chars == "ITKND":
                        row[2].value = "Счетчики посетителей ITCNT"
                    elif first_five_chars == "ITTLF":
                        row[2].value = "Телефон, факс ITTLF"
                    elif first_five_chars == "ITTCD":
                        row[2].value = "Терминал для сбора данных ITTCD,  подставки под ТСД, зарядные устройства для ТСД"
                    elif first_five_chars == "ITBOX":
                        row[2].value = "Шкаф коммутационный, серверный  ITBOX"

            wb.save(file)
            # Чтение данных из Excel-файла
            data = pd.read_excel(file, engine='openpyxl')

            # Сохранение данных в CSV-файл
            csv_file_path = os.path.join(
                upload_dir, file.name.replace(" ", "_")).replace("\\", "/")
            data.to_csv(csv_file_path, index=False)

            db_name = 'db.sqlite3'
            import_csv_to_sqlite(csv_file_path, db_name, table_name)

            os.remove(csv_file_path)

        else:
            # Сохранение загруженного CSV-файла
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(
                upload_dir, file.name.replace(" ", "_")).replace("\\", "/")
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            db_name = 'db.sqlite3'
            import_csv_to_sqlite(file_path, db_name, table_name)

            os.remove(file_path)

        return redirect('/directories/os/')


def upload_data_tmc(request):
    upload_data_os(request, table_name='Tmc')
    return redirect('/directories/tmc/')


@login_required
def Os(request):
    return render(request, 'directories/os.html')


class OsList(BaseDatatableView):
    model = apps.get_model('directories', 'IT_OS')
    columns = ['inv_dit', 'name_os', 'inpute_date',
               'os_group', 'serial_number', 'original_price']

    def render_column(self, row, column):
        # Обработка специфических столбцов (если требуется)

        if column == 'inpute_date':
            if row.inpute_date is not None:
                return row.inpute_date.strftime('%d.%m.%Y')
            else:
                return ''
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            search_terms = search_value.lower().split()
            query = Q()
            for term in search_terms:
                query |= Q(name_os__iregex=r'(?i)^.+' +
                           term[1:]) | Q(inv_dit__icontains=term)
                query |= Q(serial_number__icontains=term)
            qs = qs.filter(query)
        return qs


@login_required
def Tmc(request):
    return render(request, 'directories/tmc.html')


class TmcList(BaseDatatableView):
    model = apps.get_model('directories', 'Tmc')
    columns = ['tmc_name', 'tmc_article', 'web_code', 'tmc_price']

    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            search_terms = search_value.lower().split()
            query = Q()
            for term in search_terms:
                query |= Q(tmc_name__iregex=r'(?i)^.+' +
                           term[1:]) | Q(tmc_article__icontains=term)
                query |= Q(web_code__icontains=term)
            qs = qs.filter(query)
        return qs

def load_to_sdp(request):
    model = apps.get_model('directories', 'IT_OS')
    entries = model.objects.all()[:100]  # Получаем только первые 5 записей

    headers = {"authtoken": "DE2F5A51-D3B5-417D-99AC-2B10689E0EC0"}

    for entry in entries:
        if entry.os_group in ["Мини ПК ITEKS", "Ноутбук ITNTB", "Системный блок, Тонкий клиент ITWKS", "Моноблок ITMNB"]:
            type = "workstation"
        else:
            type = "asset"

        url = f"https://help-test/api/v3/{type}s"

        input_data = {
            type: {
                "org_serial_number": entry.serial_number,
                "name": entry.inv_dit,
                "purchase_cost": entry.original_price,
                # "department": entry.department,
                "product": {
                    "name": entry.os_group,
                },
                # "user": entry.user,
            }
        }

        data = {'input_data': json.dumps(input_data)}
        response = requests.post(url, headers=headers, data=data, verify=False)
        print(response.text)

    return HttpResponse("Data upload to SDP complete.")

