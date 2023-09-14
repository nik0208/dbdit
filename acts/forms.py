from django import forms
from .models import *
from directories.models import IT_OS
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2Widget
import re
import logging

logging.basicConfig(level=logging.DEBUG)

GROUP_CHOICES = [("", "Выберите группу ОС")] + [("Видеорегистратор","ITVDN","Видеорегистраторы ITVDN"),("Внешний жесткий диск","ITHDD","Жесткие диски ITHDD"),("ИБП","ITUPS","ИБП (источники бесперебойного питания) Стабилизатор ITUPS"),("Камера видеонаблюдения","ITVDC","Охранное видеонаблюдение (Видеокамеры ITVDC)"),("Коммутатор","ITETH","Сетевое оборудование ITETH"),("Маршрутизатор","ITETH","Сетевое оборудование ITETH"),("Мини ПК","ITEKS","Мини ПК ITEKS"),("Монитор","ITMNT","Мониторы ITMNT"),("Моноблок","ITMNB","Моноблок ITMNB"),("МФУ","ITPRN","Принтеры, МФУ, копировальные аппараты ITPRN"),("Ноутбук","ITNTB","Ноутбук ITNTB"),("Планшет","ITPAD","Планшет ITPAD"),("Принтер","ITPRN","Принтеры, МФУ, копировальные аппараты ITPRN"),("Проектор","ITPRK","Проектор ITPRK"),("Сервер","ITSRV","Сервер ITSRV"),("Система хранения данных","ITSHD","Система хранения данных ITSHD"),("Системный блок","ITWKS","Системный блок, Тонкий клиент ITWKS"),("Сканер штрихкода","ITSCN","Сканеры штрихкода ITSCN"),("Счетчик посетителей","ITCNT","Счетчики посетителей ITCNT"),("Телефон","ITTLF","Телефон, факс ITTLF"),("Тонкий клиент","ITWKS","Системный блок, Тонкий клиент ITWKS"),("Точка доступа","ITETH","Сетевое оборудование ITETH"),("ТСД","ITTCD","Терминал для сбора данных ITTCD,  подставки под ТСД, зарядные устройства для ТСД"),("Чековый принтер","ITKSS","Кассовое оборудование ITKSS"),("Шкаф серверный","ITBOX","Шкаф коммутационный, серверный  ITBOX")]

class ActForm(forms.ModelForm):

    avtor = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-field text'}))
    
                            

    def __init__(self, *args, **kwargs):
        # Получаем пользователя из аргументов
        user = kwargs.pop('user', None)
        super(ActForm, self).__init__(*args, **kwargs)
        if user:
            # Устанавливаем начальное значение поля 'avtor'
            self.initial['avtor'] = user.get_username()
        

    choses_for_type = (
        ('Замена оборудования',
         'Замена оборудования'),
        ('Замена комплектующих',
         'Замена комплектующих'),
        ('Модернизация', 'Модернизация'),
    )

    type = forms.ChoiceField(choices=choses_for_type, widget=forms.Select(
        attrs={'class': 'form-field text'}))

    class Meta:
        model = Acts
        fields = '__all__'
        field_order = ['act_date', 'avtor', 'inv_dit', 'user',
                       'result', 'conclusion', 'type', 'sklad']
        widgets = {

            "result": forms.Textarea(attrs={
                'class': 'form-field text'
            }),
            "conclusion": forms.Textarea(attrs={
                'class': 'form-field text'
            }),
            "inv_dit": ModelSelect2Widget(
                attrs={'class': 'form-field inv_dit'},
                search_fields=['inv_dit__icontains'],
            ),
            "sklad": ModelSelect2Widget(attrs={
                'class': 'form-field text'},
                search_fields=['sklad_name__icontains', 'sklad_name_lower__icontains'],
            ),
            "user": ModelSelect2Widget(attrs={
                'class': 'form-field text',
                'id': 'id_user',
                'name': 'user'},
            search_fields=['name_lower__icontains', 'name__icontains']
            ),
        }


class AddOsForm(forms.ModelForm):
    int_inv_dit = forms.CharField(max_length=50, label='Инвентарный номер', required=True, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    first_part = forms.CharField(max_length=50, label='Процессор', required=False, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    second_part = forms.CharField(max_length=50, label='ОЗУ', required=False, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    third_part = forms.CharField(max_length=50, label='Накопитель', required=False, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    model = forms.CharField(max_length=150, label='Наименование', required=False, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    department = forms.CharField(max_length=150, label='Подразделение', required=True, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    user = forms.CharField(max_length=150, label='Пользователь', required=True, widget=forms.TextInput(attrs={'class': 'form-field input'}))
    inv_dit = forms.CharField(max_length=50, label='', required=False)
    inpute_date = forms.DateTimeField(label='Дата', required=False, widget=forms.DateInput(attrs={'class': 'form-field input', 'readonly': 'readonly'}))
    os_group = forms.ChoiceField(
        choices=[(group[1], group[0]) for group in GROUP_CHOICES],
        widget=forms.Select(attrs={'class': 'form-field select'})
    )
    
    class Meta:
        model = IT_OS
        fields = ['inpute_date', 'os_group',
                  'user', 'department', 'name_os', 'inv_dit']
        
    def clean(self):
        cleaned_data = super().clean()
        int_inv_dit = cleaned_data.get('int_inv_dit')
        first_part = cleaned_data.get('first_part')
        second_part = cleaned_data.get('second_part')
        third_part = cleaned_data.get('third_part')
        os_group = cleaned_data.get('os_group')
        inv_dit = cleaned_data.get('inv_dit')
        model = cleaned_data.get('model')
        name_os = cleaned_data.get('name_os')
        
        # Найдите соответствующий кортеж с тремя элементами в GROUP_CHOICES
        selected_group = next((group for group in GROUP_CHOICES if group[1] == os_group), None)

        if selected_group:
            # Извлеките текстовое значение os_group
            os_group_text = selected_group[0]
        else:
            os_group_text = ""

        inv_dit = f"{os_group}{int_inv_dit}"


        try:
            if not name_os:
                # Используйте os_group_text для создания name_os
                if os_group_text == "Системный блок":
                    name_os = f"{os_group_text} ({first_part}\{second_part}\{third_part}) {inv_dit}"
                elif os_group_text in ["Мини ПК", "Ноутбук", "Моноблок"]:
                    name_os = f"{os_group_text} ({first_part}\{second_part}\{third_part}) {model} {inv_dit}"
                else:
                    name_os = f"{os_group_text} {model} {inv_dit}"
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
        
        cleaned_data['name_os'] = name_os
        cleaned_data['inv_dit'] = inv_dit

        return cleaned_data