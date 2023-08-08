from django import forms
from .models import *
from directories.models import IT_OS
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2Widget
import re



class ActForm(forms.ModelForm):

    avtor = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

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
        attrs={'class': 'form-field select'}))

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
                attrs={'class': 'form-field select'},
                search_fields=['inv_dit__icontains'],
            ),
            "sklad": ModelSelect2Widget(attrs={
                'class': 'form-field string'},
                search_fields=['sklad_name__icontains', 'sklad_name_lower__icontains'],
            ),
            "user": ModelSelect2Widget(attrs={
                'class': 'form-field select',
                'id': 'id_user',
                'name': 'user'},
            
            search_fields=['name_lower__icontains', 'name__icontains']
            ),
        }




class AddOsForm(forms.ModelForm):
    int_inv_dit = forms.CharField(max_length=50, label='Инвентарный номер', required=False)
    first_part = forms.CharField(max_length=50, label='Процессор', required=False)
    second_part = forms.CharField(max_length=50, label='ОЗУ', required=False)
    third_part = forms.CharField(max_length=50, label='Накопитель', required=False)
    name_os = forms.CharField(max_length=150, label='Наименование', required=False)
    inv_dit = forms.CharField(max_length=50, label='', required=False)
    inpute_date = forms.DateField(label='Дата', required=False)
    os_group = forms.Select()

    
    class Meta:
        model = IT_OS
        fields = ['inpute_date', 'os_group',
                  'user', 'department', 'name_os', 'inv_dit']
        widgets = {
            "inpute_date": forms.DateInput(attrs={
                'class': 'form-field text', 'readonly': 'readonly'
                }),
            "os_group": forms.Select(attrs={
                'label': 'Группа ОС'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        int_inv_dit = cleaned_data.get('int_inv_dit')
        first_part = cleaned_data.get('first_part')
        second_part = cleaned_data.get('second_part')
        third_part = cleaned_data.get('third_part')
        os_group = cleaned_data.get('os_group')
        inv_dit = cleaned_data.get('inv_dit')
        name_os = cleaned_data.get('name_os')

        def extract_three_letters_after_it(text):
            pattern = r'IT(\w{3})'  # Здесь \w означает "буквенно-цифровой символ", а {3} - 3 раза повторенный предыдущий шаблон.
            match = re.search(pattern, text)
            if match:
                return match.group(1)
            else:
                return None
        i = 0    
        while i < 20:
            group = GROUP_CHOICES[i]
            if os_group == group[1]:
                    inv_dit = f"IT{extract_three_letters_after_it(os_group)}{int_inv_dit}"
            i += 1
        
        try:
            if not name_os:  # Проверяем, если поле name_os пустое, то формируем его из первых трех полей
                name_os = f"Системный блок ({first_part}\{second_part}\{third_part}) {inv_dit}"
        
        except Exception as e:
            name_os = ''
        

        cleaned_data['name_os'] = name_os
        cleaned_data['inv_dit'] = inv_dit
        return cleaned_data