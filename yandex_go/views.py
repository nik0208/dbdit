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
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from docxtpl import DocxTemplate
import pandas as pd
import requests
import json

@login_required

def TaxiRequest(requests):

    url = 'https://b2b-api.go.yandex.ru/integration/2.0/orders/create'

    headers = {'Authorization': 'Bearer <OAuth-токен>',}

    data = {
    "route": [
        [start_point],
        [destination_point]
    ],
    "user_id": "035...3c71"
  }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    print(response.text)
