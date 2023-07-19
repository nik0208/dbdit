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
def Complectations(request):

    # Отрисовка HTML-шаблона с данными внутри переменной контекста context
    return render(request, 'complectations/complectations.html')


############ Создать документ комплектации ############

def AddComplectations(request):

    if request.method == 'POST':
        form = forms.ComplForm(request.POST, user=request.user)
        if form.is_valid():
            act = form.save(commit=False)
            act.avtor = request.user
            act.save()
            return redirect('complectations')
    else:
        form = forms.ComplForm(user=request.user)

    return render(request, 'complectations/add_complectations.html', {'form': form})
