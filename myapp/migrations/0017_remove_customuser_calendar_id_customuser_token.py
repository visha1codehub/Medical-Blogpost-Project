# Generated by Django 4.2.11 on 2024-03-15 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_appointment_created_time_alter_appointment_end_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='calendar_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]