from django import forms
from . import models
from django_select2.forms import Select2Widget, Select2MultipleWidget


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
        fields = ['move_num', 'user', 'sklad', 'equipment', 'comment']
        widgets = {
            "move_num": forms.TextInput(attrs={}),
            "equipment": Select2Widget(attrs={'class': 'form-field select'}),
            "sklad": Select2Widget(attrs={'class': 'form-field select'}),
            "user": Select2Widget(attrs={'class': 'form-field select'}),
            "comment": forms.TextInput(attrs={}),
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
        fields = ['move_num', 'sklad', 'user', 'equipment', 'comment', 'qty']
        widgets = {
            "move_num": forms.TextInput(attrs={}),
            "equipment": Select2Widget(attrs={'class': 'form-field select'}),
            "qty": forms.NumberInput(attrs={}),
            "sklad": Select2Widget(attrs={'class': 'form-field select'}),
            "user": Select2Widget(attrs={'class': 'form-field select'}),
            "comment": forms.TextInput(attrs={}),
        }