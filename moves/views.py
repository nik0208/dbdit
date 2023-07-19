from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.apps import apps
from openpyxl import load_workbook
from django.http import JsonResponse
from django.http import HttpResponse
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



@login_required
def Moves(request):
    return render(request, 'moves/moves.html')

class MovesList(BaseDatatableView):
    model_os = apps.get_model('moves', 'OsMove')
    model_tmc = apps.get_model('moves', 'TmcMove')
    columns = ['move_num', 'move_date', 'user', 'sklad', 'comment']

    def get_initial_queryset(self):
        os_queryset = self.model_os.objects.select_related('sklad', 'user').values(*self.columns).annotate(move_type=Value('ОС', output_field=CharField()))
        tmc_queryset = self.model_tmc.objects.select_related('sklad', 'user').values(*self.columns).annotate(move_type=Value('ТМЦ', output_field=CharField()))
        return os_queryset.union(tmc_queryset)

    def render_column(self, row, column):
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
                term_query = Q(move_num__iregex=r'(?i)^.+' + term[1:]) | Q(comment__iregex=r'(?i)^.+' + term[1:]) | Q(user__name__iregex=r'(?i)^.+' + term[1:]) | Q(sklad__sklad_name__iregex=r'(?i)^.+' + term[1:]) | Q(move_type__iregex=r'(?i)^.+' + term[1:])
                os_query |= term_query
                tmc_query |= term_query

            os_queryset = self.model_os.objects.select_related('sklad', 'user').values(*self.columns).annotate(move_type=Value('ОС', output_field=CharField())).filter(os_query)
            tmc_queryset = self.model_tmc.objects.select_related('sklad', 'user').values(*self.columns).annotate(move_type=Value('ТМЦ', output_field=CharField())).filter(tmc_query)
            qs = os_queryset.union(tmc_queryset)

        return qs

    
# Добавление перемещения OC

@login_required

def AddMove(request):
    form_os = forms.OsMoveForm(user=request.user)
    form_tmc = forms.TmcMoveForm(user=request.user)

    if request.method == 'POST':
        form_os = forms.OsMoveForm(request.POST, user=request.user)
        form_tmc = forms.TmcMoveForm(request.POST, user=request.user)

        if form_os.is_valid():
            move = form_os.save(commit=False)
            move.avtor = request.user
            move.save()
            return redirect('moves')
        
        if form_tmc.is_valid():
            move = form_tmc.save(commit=False)
            move.avtor = request.user
            move.save()
            return redirect('moves')
        
    context = {
        'form_os': form_os,
        'form_tmc': form_tmc,
    }

    return render(request, 'moves/add_move.html', context)


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
