from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


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
