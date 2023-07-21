from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from docxtpl import DocxTemplate
import win32api
import tempfile
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
import subprocess
import pandas as pd


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
    


@login_required
def Acts(request):

    # Получение всех объектов из базы данных
    all_Acts = models.Acts.objects.all().order_by('-pk')

    # Создание объекта пагинатора, указывая количество объектов на одной странице
    paginator = Paginator(all_Acts, 50)

    # Получение номера запрошенной страницы из параметров GET запроса
    page_number = request.GET.get('page')

    # Получение объектов для текущей страницы
    page_obj = paginator.get_page(page_number)

    # Отрисовка HTML-шаблона acts.html с данными внутри переменной контекста context
    return render(request, 'acts/acts.html', context={'page_obj': page_obj})


# Добавление Акта ТС
@login_required
def AddAct(request):
    
    if request.method == 'POST':
        form = forms.ActForm(request.POST, user=request.user)
        if form.is_valid():
            act = form.save(commit=False)
            act.avtor = request.user
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
# def ActDelete(request, act_id):
#     act = get_object_or_404(models.Acts, id=act_id)
#     if request.method == 'POST':
#         act.delete()
#         return redirect('acts')
#     #return render(request, 'acts/act_delete.html', {'act': act})

def ActDelete(request, act_id):
    act = get_object_or_404(models.Acts, id=act_id)
    if request.method == 'POST':
        act.delete()
        return JsonResponse({'message': 'Акт успешно удален.'})
    return JsonResponse({'error': 'Недопустимый метод запроса.'}, status=400)
    


# Печать Акта ТС
def GenerateActDocument(request, act_id):
    act = models.Acts.objects.get(id=act_id)

    # Путь к шаблону
    template_path = "G:\\.shortcut-targets-by-id\\1wDdA42V4U3psLmrHAEMLYzqdF2xgXZFK\\WebApp\\ditdb\\doki\\for_acts.docx"

    # Открытие шаблона
    document = DocxTemplate(template_path)

    # Словарь для замены
    context = {'id_act': act.pk, 'act_date': act.act_date, 'os': act.inv_dit,
               'result': act.result, 'conclusion': act.conclusion,
               'user': act.user, 'where': act.sklad, 'avtor': act.avtor}
    document.render(context)

    # Создание и сохранение изменений во временном файле
    temp_file_path = tempfile.gettempdir() + "\\generated_document.docx"

    document.save(temp_file_path)

    # Вывод на печать
    win32api.ShellExecute(0, "print", temp_file_path, None, ".", 0)

    return redirect('acts')

def CreateBasedOnAct(request, act_id):
    ...
    # Логика создания на основании акта ТС
    return redirect('acts')