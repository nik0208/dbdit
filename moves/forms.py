# forms.py
from django import forms
from . import models
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2Widget, ModelSelect2MultipleWidget


class OsMoveForm(forms.ModelForm):
    avtor = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OsMoveForm, self).__init__(*args, **kwargs)
        if user:
            self.initial['avtor'] = user.get_username()

    class Meta:
        model = models.OsMove
        fields = '__all__'
        widgets = {
            "move_num": forms.TextInput(attrs={'class': 'form-field string'}),
            "equipment": ModelSelect2Widget(queryset=models.IT_OS.objects.all(),
                                                attrs={'class': 'form-field select multi'},
                                                search_fields=['inv_dit__icontains'], ),
            "sklad": ModelSelect2Widget(queryset=models.SkladyOffice.objects.all(),
                                        attrs={'class': 'form-field select'},
                                        search_fields=['sklad_name_lower__icontains', 'sklad_name__icontains'],),
            "user": ModelSelect2Widget(attrs={'class': 'form-field select'},
                                       search_fields=['name_lower__icontains', 'name__icontains'],),
            "comment": forms.TextInput(attrs={'class': 'form-field string'},),
            "par_dok": forms.TextInput(attrs={'class': 'form-field string', 'readonly': 'readonly'},),
        }


class TmcMoveForm(forms.ModelForm):
    avtor = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TmcMoveForm, self).__init__(*args, **kwargs)
        if user:
            self.initial['avtor'] = user.get_username()

    class Meta:
        model = models.TmcMove
        fields = '__all__'
        widgets = {
            "move_num": forms.TextInput(attrs={}),
            "equipment": ModelSelect2MultipleWidget(queryset=models.Tmc.objects.all(),
                                                        attrs={'class': 'form-field select multi'},
                                                        search_fields=['tmc_name__icontains']),
            "qty": forms.NumberInput(attrs={'class': 'form-field integer'}),
            "sklad": ModelSelect2Widget(queryset=models.SkladyOffice.objects.all(),
                                        attrs={'class': 'form-field select'},
                                        search_fields=['sklad_name__icontains']),
            "user": ModelSelect2Widget(attrs={'class': 'form-field select'},
                                       search_fields=['name__icontains']),
            "comment": forms.TextInput(attrs={'class': 'form-field string'}),
        }
