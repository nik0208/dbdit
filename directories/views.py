from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from . import models
from django.apps import apps
from openpyxl import load_workbook
from django.http import JsonResponse
from django.http import HttpResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
import os
from django.conf import settings
import subprocess



@login_required
def Os(request):
    return render(request, 'directories/os.html')

class OsList(BaseDatatableView):
    model = apps.get_model('directories', 'IT_OS')
    columns = ['inv_dit', 'name_os', 'inpute_date', 'os_group', 'serial_number', 'original_price' ]

    def render_column(self, row, column):
        # Обработка специфических столбцов (если требуется)

        if column == 'inpute_date':
            if row.inpute_date is not None:
                return row.inpute_date.strftime('%Y-%m-%d')
            else:
                return ''
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        # Фильтрация данных (если требуется)
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            qs = qs.filter(name_os__icontains=search_value)
        return qs
    
@login_required
def Tmc(request):

    # Получение всех объектов из базы данных
    all_Tmc = models.Tmc.objects.all()

    # Создание объекта пагинатора, указывая количество объектов на одной странице
    paginator = Paginator(all_Tmc, 50)

    # Получение номера запрошенной страницы из параметров GET запроса
    page_number = request.GET.get('page')

    # Получение объектов для текущей страницы
    page_obj = paginator.get_page(page_number)

    # Отрисовка HTML-шаблона acts.html с данными внутри переменной контекста context
    return render(request, 'directories/tmc.html', context={'page_obj': page_obj})


def upload_data(request):

    def import_csv_to_sqlite(csv_file_path, db_name, table_name):
        # Команда для выполнения импорта CSV в SQLite
        command = f'sqlite3 {db_name} ".mode csv" ".import {csv_file_path} {table_name}"'

        # Запуск команды в терминале
        subprocess.run(command, shell=True)

    if request.method == 'POST':
        file = request.FILES['file']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        bd_name = 'db.sqlite3'
        table_name_os = 'IT_OS'
        import_csv_to_sqlite(file_path, bd_name, table_name_os)

        os.remove(file_path)

        return render(request, 'directories/os.html')
    