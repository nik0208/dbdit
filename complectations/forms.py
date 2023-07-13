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
            self.initial['avtor'] = user.get_username()  # Устанавливаем начальное значение поля 'avtor'

    class Meta:
        model = models.Complectations
        fields = ['par_doc', 'inv_dit', 'new_name_os', 'tmc', 'tmc_qty']
        widgets = {
            
            "par_doc":Select2Widget(attrs={
                'class': 'form_field_select',
                'id': 'par_doc'
            }),
            "inv_dit":Select2Widget(attrs={
                'class': 'form_field_select',
                'id': 'inv_dit',
                'name': 'inv_dit'
            }),
            "new_name_os":forms.TextInput(attrs={
                'class': 'form-field string'
            }),
            "tmc":Select2MultipleWidget(attrs={
                'class': 'form_field_multi_select'
            }),
            "tmc_qty":forms.NumberInput(attrs={
                'class': 'form_field_num'
            }),
        }
        