from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from . import forms
from .models import *
from django.apps import apps
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q, F, Value, CharField
from django.shortcuts import render, get_object_or_404, redirect
from docxtpl import DocxTemplate
import win32api
import tempfile
from django.db.models import CharField
import os
import datetime
import xlrd
from django.core.files.storage import FileSystemStorage
import logging
from datetime import datetime
import send2trash
from django.db import transaction

logging.basicConfig(level=logging.DEBUG)


@login_required
def Moves(request):
    return render(request, 'moves/moves.html')


class MovesList(BaseDatatableView):
    model_os = apps.get_model('moves', 'OsMove')
    model_tmc = apps.get_model('moves', 'TmcMove')
    columns = ['move_num',
               'move_date', 'user', 'sklad', 'comment']

    def get_initial_queryset(self):
        os_queryset = self.model_os.objects.select_related('sklad', 'user').values(
            *self.columns).annotate(move_type=Value('ОС', output_field=CharField()))
        tmc_queryset = self.model_tmc.objects.select_related('sklad', 'user').values(
            *self.columns).annotate(move_type=Value('ТМЦ', output_field=CharField()))
        return os_queryset.union(tmc_queryset)

    def render_column(self, row, column):

        if column == 'equipment_os':
            return ', '.join([str(equipment) for equipment in row['equipment_os'].all()])

        if column == 'move_date':
            if row['move_date'] is not None:
                return row['move_date'].strftime('%d.%m.%Y')
            else:
                return ''
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            search_terms = search_value.lower().split()
            os_query = Q()
            tmc_query = Q()
            for term in search_terms:
                term_query = Q(move_num__iregex=r'(?i)^.+' + term[1:]) | Q(comment__iregex=r'(?i)^.+' + term[1:]) | Q(
                    user__name__iregex=r'(?i)^.+' + term[1:]) | Q(sklad__sklad_name__iregex=r'(?i)^.+' + term[1:]) | Q(move_type__iregex=r'(?i)^.+' + term[1:])
                os_query |= term_query
                tmc_query |= term_query

            os_queryset = self.model_os.objects.select_related('sklad', 'user').values(
                *self.columns).annotate(move_type=Value('ОС', output_field=CharField())).filter(os_query)
            tmc_queryset = self.model_tmc.objects.select_related('sklad', 'user').values(
                *self.columns).annotate(move_type=Value('ТМЦ', output_field=CharField())).filter(tmc_query)
            qs = os_queryset.union(tmc_queryset)

        return qs


def get_move_details(request, move_pk):

    # Предполагается, что move_pk - это значение PK из строки таблицы
    move = models.OsMove.objects.get(pk=move_pk)
    context = {'move': move}
    return render(request, 'moves/move_details.html', context)

# Добавление перемещения OC


@login_required
def AddMoveOS(request):
    if request.method == 'POST':
        form = forms.OsMoveForm(request.POST, user=request.user)
        if form.is_valid():
            move_os = form.save(commit=False)
            move_os.avtor = request.user
            move_os.save()
            form.save_m2m()  # Сохранение связанных полей
            return redirect('moves')
    else:
        form = forms.OsMoveForm(user=request.user)

    return render(request, 'moves/add_move_os.html', {'form': form})


@login_required
def AddMoveTmc(request):
    if request.method == 'POST':
        form = forms.TmcMoveForm(request.POST, user=request.user)
        if form.is_valid():
            move_tmc = form.save(commit=False)
            move_tmc.avtor = request.user
            move_tmc.save()
            form.save_m2m()  # Сохранение связанных полей
            return redirect('moves')
    else:
        form = forms.TmcMoveForm(user=request.user)

    return render(request, 'moves/add_move_tmc.html', {'form': form})

# Печать путевого листа


def GenerateMoveDocument(request, move_id):
    move = models.OsMove.objects.get(id=move_id)

    # Путь к шаблону
    template_path = os.path.join('doki', 'way_list.docx')

    # Открытие шаблона
    document = DocxTemplate(template_path)

    # Словарь для замены
    context = {'move_num': move.move_num, 'sklad': move.sklad.sklad_name, 'user': move.user,
               'phone_num': move.user.phone_num, 'city': move.sklad.sklad_city,
               'adres': move.sklad.sklad_adress}
    document.render(context)

    # Создание и сохранение изменений во временном файле
    temp_file_path = tempfile.gettempdir() + "\\generated_document.docx"

    document.save(temp_file_path)

    # Вывод на печать
    win32api.ShellExecute(0, "print", temp_file_path, None, ".", 0)

    return redirect('moves')


def upload_data_move(request, table_name='OS_move'):

    @transaction.atomic
    def import_OSxls_to_sqlite(move_num, names, sklad_name, date):

        # Вставка новых данных
        OsMove.objects.create(
            move_num=move_num,
            move_date=date,
            avtor='User',
            sklad=sklad_name,
            user_id='Никита Федоров',
            equipment_id=names
        )

    @transaction.atomic
    def import_TMCxls_to_sqlite(move_num, names, sklad_name, date):

        # Вставка новых данных
        TmcMove.objects.create(
            move_num=move_num,
            move_date=date,
            avtor='User',
            sklad=sklad_name,
            user_id='Никита Федоров',
            equipment_id=names
        )
    
    
    folder = request.FILES.getlist('folder')
    logging.debug(f"Folder: {folder}")

    fs = FileSystemStorage(location='invoices/')

    for file in folder:
        try:
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            logging.debug(f"Filename: {filename}, File path: {file_path}")

            workbook = xlrd.open_workbook(file_path)
            sheet = workbook.sheet_by_index(0)

            osmove_value = "Приложение 19"
            tmcmove_value = "Приложение 29"


            for row in range(sheet.nrows):
                for col in range(sheet.ncols):
                    
                    cell_value = sheet.cell_value(row, col)

                    if cell_value == osmove_value:

                        logging.debug(f"move_value: {osmove_value}, cell_value: {cell_value}")
                        
                        desired_value = "Всего отпущено количество (прописью)"
                        for row in range(sheet.nrows):
                            for col in range(sheet.ncols):
                                cell_value = sheet.cell_value(row, col)
                                if cell_value == desired_value:
                                    # os_path = sheet.cell_value(row, col)
                                    os_qty = sheet.cell_value(row - 2, col)

                        logging.debug(f"os_qty: {os_qty}")

                        os_names = []
                        for i in range(int(os_qty)):
                            a = sheet.cell_value(25 + i, 2)
                            last_i_index = a.rfind('I')

                            if last_i_index != -1:
                                # Получаем подстроку от первой "I" с конца до конца строки
                                itm_code = a[last_i_index:]

                            while not itm_code[-1].isdigit():
                                itm_code = itm_code.rstrip(itm_code[-1])
                            os_names.append(itm_code)
                        
                        logging.debug(f"os_names: {os_names}")
                    
                        move_num = sheet.cell_value(20, 16)
                        sklad = sheet.cell_value(11, 6)
                        date = sheet.cell_value(20, 27)

                        logging.debug(f"move_num: {move_num}, sklad: {sklad}, date: {date}")

                        # Создание словаря для месяцев на русском
                        month_names = {
                            "января": 1,
                            "февраля": 2,
                            "марта": 3,
                            "апреля": 4,
                            "мая": 5,
                            "июня": 6,
                            "июля": 7,
                            "августа": 8,
                            "сентября": 9,
                            "октября": 10,
                            "ноября": 11,
                            "декабря": 12,
                        }

                        # Разбор даты
                        date_parts = date.split()
                        day = int(date_parts[0])
                        month = month_names[date_parts[1]]
                        year = int(date_parts[2])

                        # Создание объекта datetime
                        date_obj = datetime(year, month, day)

                        # Форматирование в цифровой формат
                        formatted_date = date_obj.strftime('%Y-%m-%d')

                        logging.debug(f"formatted_date: {formatted_date}")

                        for os_name in os_names:
                            logging.debug(
                                f"Calling import_xls_to_sqlite with os_name={os_name}")
                            import_OSxls_to_sqlite(
                                move_num, os_name, sklad, formatted_date)
                            
                        os.remove(file_path)
                        
                            
                    elif cell_value == tmcmove_value:
                        desired_value = "Всего отпущено количество (прописью)"
                        for row in range(sheet.nrows):
                            for col in range(sheet.ncols):
                                cell_value = sheet.cell_value(row, col)
                                if cell_value == desired_value:
                                    # os_path = sheet.cell_value(row, col)
                                    os_qty = int(sheet.cell_value(row - 4, col))

                        logging.debug(f"os_qty: {range(os_qty)}")
                        os_names = []
                    
                        def custom_encode(s):
                            replacements = {
                                ' ': '',
                            }
                            
                            result = []
                            for char in s:
                                result.append(replacements.get(char, char))
                            
                            return ''.join(result)
                    
                        for i in range(os_qty):

                            a = sheet.cell_value(24 + i, 21)


                        
                            a = custom_encode(a)
                            os_names.append(a)

                        logging.debug(f"os_names: {os_names}")

                        move_num = sheet.cell_value(11, 34)
                        sklad = sheet.cell_value(18, 18)
                        date_value = sheet.cell_value(11, 41)

                        logging.debug(f"move_num: {move_num}, sklad: {sklad}, date: {date_value}")

                        logging.debug(f"Type of os_qty: {type(os_qty)}")
                        logging.debug(f"Type of date_value: {type(date_value)}")


                        formatted_date = datetime.strptime(date_value, "%d.%m.%Y").strftime("%Y-%m-%d")

                        
                        for os_name in os_names:

                            logging.debug(
                                                f"Calling import_xls_to_sqlite with os_name={os_name}")

                            import_TMCxls_to_sqlite(
                                move_num, os_name, sklad, formatted_date)
                            
                        os.remove(file_path)

    
        
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
            continue

    return redirect('/moves')
