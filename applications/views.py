from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from . import models
#from . import forms
from django.contrib.auth.decorators import login_required


@login_required
def Application(request):

    # Получение всех объектов из базы данных
    all_Applications = models.Applications.objects.all().order_by('-pk')

    # Создание объекта пагинатора, указывая количество объектов на одной странице
    paginator = Paginator(all_Applications, 50)

    # Получение номера запрошенной страницы из параметров GET запроса
    page_number = request.GET.get('page')

    # Получение объектов для текущей страницы
    page_obj = paginator.get_page(page_number)

    # Отрисовка HTML-шаблона acts.html с данными внутри переменной контекста context
    return render(request, 'applications/applications.html', context={'page_obj': page_obj})