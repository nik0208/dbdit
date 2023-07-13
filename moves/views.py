from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from docxtpl import DocxTemplate
import win32api
import tempfile


@login_required
def Moves(request):

    os_moves = models.OsMove.objects.values(
        'id', 'move_num', 'move_date', 'user', 'sklad', 'comment')
    tmc_moves = models.TmcMove.objects.values(
        'id', 'move_num', 'move_date', 'user', 'sklad', 'comment')

    combined = list(os_moves.union(tmc_moves, all=True))

    combined.sort(key=lambda x: x['move_date'], reverse=True)

    # Создание объекта пагинатора, указывая количество объектов на одной странице
    paginator = Paginator(combined, 50)

    # Получение номера запрошенной страницы из параметров GET запроса
    page_number = request.GET.get('page')

    # Получение объектов для текущей страницы
    page_obj = paginator.get_page(page_number)

    context = {
        'combined': combined
    }

    return render(request, 'moves/os_move.html', context)


# Добавление перемещения OC
@login_required
def AddOsMove(request):
    if request.method == 'POST':
        form = forms.OsMoveForm(request.POST, user=request.user)
        if form.is_valid():
            osmove = form.save(commit=False)
            osmove.avtor = request.user
            osmove.save()
            return redirect('moves')
    else:
        form = forms.OsMoveForm(user=request.user)
    return render(request, 'moves/add_os_move.html', {'form': form})


# Добавление перемещения ТМЦ
@login_required
def AddTmcMove(request):
    if request.method == 'POST':
        form = forms.TmcMoveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('moves')
    else:
        form = forms.TmcMoveForm()
    return render(request, 'moves/add_tmc_move.html', {'form': form})


# Печать путевого листа
def GenerateMoveDocument(request, move_id):
    move = models.OsMove.objects.get(id=move_id)

    # Путь к шаблону
    template_path = "G:\\.shortcut-targets-by-id\\1wDdA42V4U3psLmrHAEMLYzqdF2xgXZFK\\WebApp\\ditdb\\doki\\way_list.docx"

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
