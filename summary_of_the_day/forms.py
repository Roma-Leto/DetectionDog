import datetime

from django import forms
from .models import Cigarettes, PullUpsModel
from django.core.validators import MinValueValidator, MaxValueValidator


class AddCigarettesForm(forms.Form):
    data = forms.DateField(label="Дата",
                           initial=datetime.datetime.now(),
                           widget=forms.DateInput(
                               format='%Y-%m-%d',
                               attrs={'class': 'form-control',
                                      'placeholder': 'Select a date',
                                      'type': 'date'
                                      }),
                           )
    count = forms.IntegerField(
        label="Количество",
        min_value=0,
        required=False,
        error_messages={
            'min_value': 'Недопустимо низкое значение.',
            'required': 'Не может быть пустым'
        },
        validators=[
            MaxValueValidator(60, message="Слишком большое число"),
        ],
    )


class AddPullUpsForm(forms.ModelForm):

    class Meta:
        model = PullUpsModel
        fields = [
            'data',
            'count',
            'number_of_approaches'
        ]
        widgets = {
            'data': forms.DateInput(
                               format='%Y-%m-%d',
                               attrs={'class': 'form-control',
                                      'placeholder': 'Select a date',
                                      'type': 'date'
                                      }),
        }