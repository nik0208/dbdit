from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.apps import apps
from openpyxl import load_workbook
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
import os
from django.conf import settings
import subprocess
from django.db.models import Q, F, Value, CharField
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from docxtpl import DocxTemplate
import win32api
import tempfile
from django.db.models.functions import Lower
from django.db.models import CharField
from django.contrib import messages
import pandas as pd
from datetime import date
import datetime
from directories.models import Users
from django.db import connection


@login_required
def Acts(request):
    return render(request, 'acts/acts.html')

def reset_sequence(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM {table_name}) WHERE name='{table_name}';")


class ActsList(BaseDatatableView):
    model = apps.get_model('acts', 'Acts')
    columns = ['pk', 'act_date', 'inv_dit_id', 'result',
               'conclusion', 'type', 'new_user_id', 'avtor', 'new_sklad_id']

    def render_column(self, row, column):
        # Обработка специфических столбцов (если требуется)

        if column == 'act_date':
            if row.act_date is not None:
                return row.act_date.strftime('%d.%m.%Y')
            else:
                return ''
        elif column == 'new_user_id':

            if isinstance(row.new_user_id, int):
                # Получение экземпляра пользователя
                user_instance = Users.objects.get(id=row.new_user_id)
                return user_instance.name
            elif row.new_user_id is None:
                user_instance = models.Acts.objects.get(id=row.pk)
                return user_instance.user

        elif column == 'new_sklad_id':
            if row.new_sklad_id is None:
                sklad_instance = models.Acts.objects.get(id=row.pk)
                return sklad_instance.sklad

        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            search_terms = search_value.lower().split()
            query = Q()
            for term in search_terms:
                query |= Q(inv_dit_id__inv_dit__iregex=f'(?i).*{term}.*') | Q(new_user_id__name__iregex=f'(?i).*{term}.*') | Q(conclusion__iregex=f'(?i).*{term}.*') | Q(
                    avtor__iregex=f'(?i).*{term}.*') | Q(new_sklad_id__sklad_name__iregex=f'(?i).*{term}.*') | Q(id__iregex=f'(?i).*{term}.*') | Q(user__iregex=f'(?i).*{term}.*') | Q(sklad__iregex=f'(?i).*{term}.*')
                    
            qs = qs.filter(query)
        return qs



# Добавление Акта ТС


@login_required
def AddAct(request):

    if request.method == 'POST':
        form = forms.ActForm(request.POST, user=request.user)
        if form.is_valid():
            act = form.save(commit=False)
            act.avtor = f"{request.user.last_name} {request.user.first_name}"
            act.save()
            return redirect('acts')
    else:
        form = forms.ActForm(user=request.user)

    return render(request, 'acts/add_act.html', {'form': form})


# Информация по старым актам
def get_acts(request):
    inv_dit = request.GET.get('inv_dit')

    acts = models.Acts.objects.filter(inv_dit__inv_dit=inv_dit).values()

    return JsonResponse({'acts': list(acts)})


@login_required
# Изменение Акта ТС
def ActEdit(request, act_id):
    act = get_object_or_404(models.Acts, id=act_id)

    a = f'{request.user.last_name} {request.user.first_name}'

        # Проверка того, является ли пользователь автором
    if not request.user.groups.filter(name='Склад').exists() and act.avtor != a:
        return HttpResponseForbidden("Вы не являетесь автором этого акта, и поэтому не можете его редактировать.")
    
    if request.method == 'POST':
        form = forms.ActForm(request.POST, instance=act)
        if form.is_valid():
            form.save()
            return redirect('acts')
    else:
        form = forms.ActForm(instance=act)
    return render(request, 'acts/act_edit.html', {'form': form, 'act': act})


@login_required
# Удаление Акта ТС
def has_related_objects(instance):
    fields = instance._meta.get_fields()
    for field in fields:
        if isinstance(field, models.ForeignKey):
            related_objects = getattr(instance, field.name).all()
            if related_objects.exists():
                return True
    return False


def ActDelete(request, act_id):
    act = get_object_or_404(models.Acts, id=act_id)

    if not request.user.groups.filter(name='Склад').exists():
        print(request.user.groups.all())
        return JsonResponse({'success': False, 'message': 'У вас нет прав на удаление этого акта'})
    else:
        try:
            if request.method == 'POST':
                act.delete()
                reset_sequence('Acts')
                return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False, 'message': 'Произошла ошибка при удалении.'})


def GenerateActDocument(request, act_id):
    act = models.Acts.objects.get(id=act_id)
    template_path = os.path.join('doki', 'for_acts.docx')
    document = DocxTemplate(template_path)
    act_date = act.act_date.strftime('%d.%m.%Y')

    context = {'id_act': act.pk, 'act_date': act_date, 'os': act.inv_dit,
               'result': act.result, 'conclusion': act.conclusion,
               'user': act.new_user, 'where': act.new_sklad, 'avtor': act.avtor}

    document.render(context)

    # Сохранение во временный файл
    temp_file_path = os.path.join(
        tempfile.gettempdir(), "generated_document.docx")
    document.save(temp_file_path)

    # Чтение файла для ответа
    with open(temp_file_path, 'rb') as f:
        response = HttpResponse(f.read(
        ), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'inline; filename=generated_document.docx'
        return response


def CreateBasedOnAct(request, act_id):
    ...
    # Логика создания на основании акта ТС
    return redirect('acts')


def upload_data_acts(request, table_name='Acts'):

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

        return redirect('/acts')


def add_os(request):
    today = datetime.date.today()
    if request.method == 'POST':
        form = forms.AddOsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/acts/addact')
        else:
            pass
    else:

        initial_data = {
            'inpute_date': today,  # Устанавливаем дату по умолчанию
            'model': "None",
            'first_part': None,
            'second_part': None,
            'third_part': None,
        }
        form = forms.AddOsForm(initial=initial_data)

    return render(request, 'acts/add_os.html', {'form': form})
