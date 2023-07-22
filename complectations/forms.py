from django import forms
from . import models
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2Widget, ModelSelect2MultipleWidget


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
            # Остальные виджеты
            "inv_dit": ModelSelect2Widget(
                attrs={'class': 'form-field select'}, search_fields=['inv_dit__icontains'],
            ),
            "new_name_os": forms.TextInput(attrs={}),
            "tmc": ModelSelect2MultipleWidget(attrs={'class': 'form-field select multi'}, search_fields=['tmc_name__icontains'],
            ),
            "tmc_qty": forms.NumberInput(attrs={}),
        }
