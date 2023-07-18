from django import forms
from .models import *
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
        model = OsMove
        fields = '__all__'
        widgets = {
            "equipment":Select2MultipleWidget(attrs={
                'class': 'form_field select multi', 
                'id': 'equipment'
            }),

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
        model = TmcMove
        fields = '__all__'
        widgets = {
            "equipment":Select2MultipleWidget(attrs={
                'class': 'form_field select multi',
                'id': 'equipment'
            }),
            "qty":forms.NumberInput(attrs={
                'class': 'form_field num'
            }),
        }
