from django.db import models
from datetime import timedelta, datetime, date, time
from user.models import CustomUser


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

