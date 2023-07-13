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
import win32api
import tempfile

@login_required
def Moves(request):
    return render(request, 'moves/moves.html')
    
    moves = models.OsMove.objects.values(
        'id', 'move_num', 'move_date', 'user', 'sklad', 'comment')
    tmc_moves = models.TmcMove.objects.values(
        'id', 'move_num', 'move_date', 'user', 'sklad', 'comment')

    combined = list(moves.union(tmc_moves, all=True))

    combined.sort(key=lambda x: x['move_date'], reverse=True)

    context = {
        'combined': combined
    }

class MovesList(BaseDatatableView):
    model_os = apps.get_model('moves', 'OsMove')
    model_tmc = apps.get_model('moves', 'TmcMove')
    columns = ['move_num', 'move_date', 'status', 'sklad', 'user', 'comment']

    def render_column(self, row, column):
        if column == 'move_date':
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
                query |= Q(name_os__iregex=r'(?i)^.+' + term[1:])
            qs = qs.filter(query)
        return qs

# Добавление перемещения OC
@login_required
def AddMove(request):
    if request.method == 'POST':
        form = forms.OsMoveForm(request.POST, user=request.user)
        if form.is_valid():
            osmove = form.save(commit=False)
            osmove.avtor = request.user
            osmove.save()
            return redirect('moves')
    else:
        form = forms.OsMoveForm(user=request.user)
    return render(request, 'moves/add_moves.html', {'form': form})


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
