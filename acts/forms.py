from django import forms
from . import models
from django_select2.forms import Select2Widget, Select2MultipleWidget


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
        model = models.Acts
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
            "inv_dit": Select2Widget(attrs={
                'class': 'form_field_select',
                'id': 'id_inv_dit',
                'name': 'inv_dit'
            }),
            "sklad": forms.Select(attrs={
                'class': 'form-field string'
            }),
            "user": Select2Widget(attrs={
                'class': 'form_field_select',
                'id': 'id_user',
                'name': 'user'
            }),
        }
