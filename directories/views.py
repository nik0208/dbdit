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


