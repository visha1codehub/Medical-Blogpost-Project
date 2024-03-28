from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment
from .utils import createEvent
from user.decorators import patient_required
from user.models import CustomUser


import os
import google_apis_oauth
from googleapiclient.discovery import build


REDIRECT_URI = 'http://localhost:8000/appointment/google_oauth/callback/'

SCOPES = ['https://www.googleapis.com/auth/calendar']

JSON_FILEPATH = os.path.join(os.getcwd(), 'client_id.json')
USER = ""
def RedirectOauthView(request):
    global USER
    USER = request.user
    token = USER.token
    if token:
        return HttpResponseRedirect("https://calendar.google.com/calendar")
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    print(oauth_url)
    return HttpResponseRedirect(oauth_url)


def CallbackView(request):
    # Get user credentials
    credentials = google_apis_oauth.get_crendentials_from_callback(
        request,
        JSON_FILEPATH,
        SCOPES,
        REDIRECT_URI
    )
    # Stringify credentials for storing them in the DB
    stringified_token = google_apis_oauth.stringify_credentials(credentials)
    # print(user.id)
    USER.token = stringified_token
    USER.save()
    return HttpResponseRedirect("https://calendar.google.com/calendar")




@login_required(login_url='login')
@patient_required
def appointment_form(request, doc_id):
    form = AppointmentForm()
    patient = request.user
    doctor = CustomUser.objects.get(id=doc_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.save()
            createEvent(appointment)
            return redirect('appointment-detail',pk=appointment.id)
    context = {'form':form}
    return render(request, 'appointment/appointment_form.html', context)




@login_required(login_url='login')
def appointment_detail(request, pk):
    appointment = Appointment.objects.get(id=pk)
    context = {'appointment':appointment}
    return render(request, 'appointment/appointment_detail.html', context)




@login_required(login_url='login')
def appointment_list(request):
    user = request.user
    if user.user_type == 'patient':
        appointments = user.appointment_set.all()
    else:
        appointments = user.doc_appointments.all()
    context = {'appointments':appointments}
    return render(request, 'appointment/appointments_list.html', context)
