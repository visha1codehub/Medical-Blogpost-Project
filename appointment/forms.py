from django import forms
from .models import Appointment
from datetime import date




class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['speciality', 'date', 'start_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'min': '09:00', 'max': '18:00'}),
        }
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"form-control"})
