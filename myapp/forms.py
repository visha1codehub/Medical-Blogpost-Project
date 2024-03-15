from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, BlogPost, Appointment
from datetime import date


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
                  'user_type',
                  'first_name',
                  'last_name',
                  'profile_picture',
                  'username',
                  'email',
                  'password1',
                  'password2',
                  'address_line1',
                  'city',
                  'state',
                  'pincode'
                  ]
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"form-control"})


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
                  'title',
                  'image',
                  'category',
                  'summary',
                  'content',
                  ]
        widgets = {
          'summary': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"form-control"})


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