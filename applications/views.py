from django.contrib.auth.decorators import login_required
from .models import *
from django.apps import apps
from django_datatables_view.base_datatable_view import BaseDatatableView
import os
from django.conf import settings
import subprocess
from django.db.models import Q, F, Value, CharField
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from . import forms
from datetime import date
import datetime
import locale
from django.http import HttpResponse
import requests
from lxml import html
import sys
from bs4 import BeautifulSoup as bs


@login_required
def Application(request):
    return render(request, 'applications/applications.html')

class ApplicationsList(BaseDatatableView):
    model = apps.get_model('applications', 'Applications')
    columns = ['num', 'requested_equipment', 'avtor', 'user', 'date', 'deadline', 'department', 'status']

    def update_status(request, pk):
        if request.method == 'POST':
            new_status = request.POST.get('status')
            application = get_object_or_404(Applications, pk=pk)
            application.status = new_status
            application.save()
            return HttpResponse('Статус обновлен успешно.')
        return HttpResponse(status=400)

    def render_column(self, row, column):
        # Обработка специфических столбцов (если требуется)

        if column == 'date':
            if row.date is not None:
                return row.date.strftime('%d.%m.%Y')
            else:
                return ''
        
        if column == 'deadline':
            if row.deadline is not None:
                return row.deadline.strftime('%d.%m.%Y')
            else:
                return ''
    
        return super().render_column(row, column)

    
    
    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            search_terms = search_value.lower().split()
            query = Q()
            for term in search_terms:
                query |= Q(num__iregex=r'(?i)^.+' + term[1:]) | Q(avtor__iregex=r'(?i)^.+' + term[1:]) | Q(user__iregex=r'(?i)^.+' + term[1:]) | Q(department__icontains=term[1:])
            qs = qs.filter(query)
        return qs
    
    
    
    
def upload_data_appl(request, table_name='Applications'):

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

        return redirect('/applications')
    


@login_required
def AddAppl(request):

    if request.method == 'POST':
        
        username = 'jkaq'
        password = 'Ытщц201820_'


        auth = requests.auth.HTTPBasicAuth(username, password.encode('utf-8'))

        def parse(url):

            response = requests.get(url, auth=auth)

            if response.status_code == 200:
                soup = bs(response.text, "html.parser")
                text = soup.find_all('td', class_='bx-bizproc-sorted')
                text = text[::3]
                symbols_to_remove = ['<b>', '</b>', '</br>', '<br/>', '</td>', '<br>']
                
                for i in text:

                    i = str(i)
                    for symbol in symbols_to_remove:
                        i = i.replace(symbol, " ")

                    i = i.split(sep=' ')

                    

                    i = [k for k in i if len(k) > 1]

                    print(i)
                    if 'Заявка на организацию рабочего места' in i[1]:
                        req_eqipment = i[i.index('Необходимое оборудование:') + 1:(i.index('Необходимое оборудование:') + 1) + 6]
                        usr = i[i.index('Фамилия:'):i.index('Фамилия:') + 6]
                        a = i[i.index('Дата выхода:') + 1].strip()
                        a = a.split(sep='.')
                        b = [a[2], a[1], a[0]]
                        b = '-'.join(b)
                        #new_date_str = datetime.strptime(a, "%Y-%m-%d")
                        Applications.objects.update_or_create(
                            num = i[1].split('№')[1],
                            
                            requested_equipment = str(f'{req_eqipment[0]} {req_eqipment[1]} \n {req_eqipment[2]} {req_eqipment[3]} \n {req_eqipment[4]} {req_eqipment[5]}'),
                            avtor = i[i.index('Автор:') + 1].split(') ')[1].strip(),
                            user = str(f'{usr[0]} {usr[1]} \n {usr[2]} {usr[3]} \n {usr[4]} {usr[5]}'),
                            deadline = b,
                            department = i[i.index('Подразделение:') + 1].strip(),
                        )
                    elif 'Заявка на ИТ оборудование' in i[1]:
                        req_eqipment = i[i.index('Необходимое оборудование'):i.index('Обоснование')]
                        newreq_eqipment = ''
                        for q in req_eqipment:
                            newreq_eqipment += q + '\n'
                        Applications.objects.update_or_create(
                            num = i[1].split('№')[1],
                            requested_equipment = newreq_eqipment,
                            avtor = i[i.index('Автор:') + 1].split(') ')[1],
                            user = i[i.index('Для кого закуп') + 1].split(') ')[1],
                            department = i[i.index('Подразделение') + 1].split(': ')[1],
                        )

                    
            else:
                print(f"Ошибка при запросе: {response.status_code}")

        def main():
            parse('https://technet.technodom.kz/company/personal/bizproc/')

        
        main()



















    #     form = forms.ApplForm(request.POST)
    #     if form.is_valid():
    #         act = form.save()
    #         act.save()
    #         return redirect('/applications')
    #     else:
    #         print(form.errors)
    # else:
    #     initial_data = {

    #         'num': "1",
    #         'requested_equipment': "1",
    #         'avtor': "1",
    #         'user': "1",
    #         'department': "1",
    #     }
    #     form = forms.ApplForm(initial=initial_data)

    return redirect('/applications')

def UpdateStatus(request, pk):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application = get_object_or_404(Applications, pk=pk)
        application.status = new_status
        application.save()
        return HttpResponse('Статус обновлен успешно.')
    return HttpResponse(status=400)