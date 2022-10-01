from django import forms

from .models import DateRange


class DateInput(forms.DateInput):
    input_type = 'date'


class DateRangeForm(forms.ModelForm):
    class Meta:
        model = DateRange
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
