from django import forms
from . import models
from directories.models import IT_OS
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2Widget, ModelSelect2MultipleWidget


class ComplForm(forms.ModelForm):
    
    prev_name_os = forms.CharField(widget=forms.TextInput(attrs={'id': 'prev_name'})
                                   )

    avtor = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя из аргументов
        super(ComplForm, self).__init__(*args, **kwargs)
        if user:
            # Устанавливаем начальное значение поля 'avtor'
            self.initial['avtor'] = user.get_username()

    class Meta:
        model = models.Complectations
        fields = ['par_doc', 'inv_dit', 'new_name_os', 'tmc', 'tmc_qty','prev_name_os']
        widgets = {
            "inv_dit": ModelSelect2Widget(
                attrs={'class': 'form-field inv_dit',
                       }, 
                       search_fields=['inv_dit__icontains'],
            ),
            "new_name_os": forms.TextInput(attrs={'class': 'form-field text', 'id': 'new_name_os'}),
            "par_doc": ModelSelect2Widget(attrs={'class': 'form-field text'}),
            "tmc": ModelSelect2MultipleWidget(attrs={'class': 'form-field select multi'}, search_fields=['tmc_name__icontains'],
            ),
            "tmc_qty": forms.NumberInput(attrs={}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        new_name_os = self.cleaned_data.get('new_name_os')
        
        if new_name_os:
            it_os_instance = instance.inv_dit
            it_os_instance.name_os = new_name_os
            it_os_instance.save()

        if commit:
            instance.save()
        return instance
