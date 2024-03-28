from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHIOCE = (
        ('doctor', "Doctor"),
        ('patient', "Patient")
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHIOCE, default='patient')
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    profile_picture = models.ImageField(default='avatar.svg')
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    pincode = models.CharField(max_length=20)
    token = models.CharField(max_length=1500, null=True, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url
