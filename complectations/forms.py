from django import forms
from . import models
from django_select2.forms import Select2Widget, Select2MultipleWidget


class ComplForm(forms.ModelForm):

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
        fields = ['par_doc', 'inv_dit', 'new_name_os', 'tmc', 'tmc_qty']
        widgets = {

            "par_doc": Select2Widget(attrs={'class': 'form-field select'}),
            "inv_dit": Select2Widget(attrs={'class': 'form-field select'}),
            "new_name_os": forms.TextInput(attrs={}),
            "tmc": Select2MultipleWidget(attrs={'class': 'form-field select multi'}),
            "tmc_qty": forms.NumberInput(attrs={}),
        }
