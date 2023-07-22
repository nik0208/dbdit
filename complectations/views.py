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
from django.contrib import messages
import pandas as pd


@login_required
def Complectations(request):
    return render(request, 'complectations/complectations.html')

class ComplectationsList(BaseDatatableView):
    model = apps.get_model('complectations', 'Complectations')
    columns = ['pk', 'date', 'avtor', 'inv_dit', 'tmc', 'tmc_qty', 'par_doc']

    def render_column(self, row, column):
        # Обработка специфических столбцов (если требуется)

        if column == 'date':
            if row.date is not None:
                return row.date.strftime('%d.%m.%Y')
            else:
                return ''
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', '')
        if search_value:
            search_terms = search_value.lower().split()
            query = Q()
            for term in search_terms:
                query |= Q(inv_dit__inv_dit__iregex=r'(?i)^.+' + term[1:]) | Q(tmc__tmc_name__iregex=r'(?i)^.+' + term[1:])
            qs = qs.filter(query)
        return qs


############ Создать документ комплектации ############

def AddComplectations(request):

    if request.method == 'POST':
        form = forms.ComplForm(request.POST, user=request.user)
        if form.is_valid():
            act = form.save(commit=False)
            act.avtor = request.user
            act.save()
            form.save_m2m()
            return redirect('complectations')
    else:
        form = forms.ComplForm(user=request.user)

    return render(request, 'complectations/add_complectations.html', {'form': form})