from django.contrib.auth.decorators import login_required
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
def Application(request):
    return render(request, 'applications/applications.html')

class ApplicationsList(BaseDatatableView):
    model = apps.get_model('applications', 'Applications')
    columns = ['num', 'requested_equipment', 'avtor', 'user', 'date', 'deadline', 'department', 'status']

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