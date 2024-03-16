from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime, date, time

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


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    def __str__(self):
        return self.title


class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doc_appointments')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default=time(hour=0, minute=0))
    created_time = models.DateTimeField(auto_now_add=True, null=True)


    def save(self, *args, **kwargs):
        start = datetime.combine(date.today(), self.start_time)
        self.end_time = (start + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.speciality} - {self.date} - {self.start_time} to {self.end_time}"

