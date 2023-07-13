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

    all_Complectaions = models.Complectations.objects.all().order_by('-pk')

    # Создание объекта пагинатора, указывая количество объектов на одной странице
    paginator = Paginator(all_Complectaions, 50)
    
    # Получение номера запрошенной страницы из параметров GET запроса
    page_number = request.GET.get('page')

    # Получение объектов для текущей страницы
    page_obj = paginator.get_page(page_number)

    # Отрисовка HTML-шаблона с данными внутри переменной контекста context
    return render(request, 'complectations/complectations.html', context={'page_obj': page_obj})

############ Создать документ комплектации ############
def AddComplectations (request):

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