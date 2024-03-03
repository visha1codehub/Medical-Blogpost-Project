from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import SignUpForm
from .models import CustomUser
from .decorators import doctor_required


# Create your views here.

def home(request):
    return render(request, 'myapp/home.html')

def signupPage(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.user_type == "doctor":
                return redirect('doctor-dashboard')
            else:
                return redirect('patient-dashboard')
        else:
            return HttpResponse("<h1>Invalid Inputs!!!!</h1>")
    context = {'form' : form }
    return render(request, 'myapp/signup.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == "doctor":
                return redirect('doctor-dashboard')
            else:
                return redirect('patient-dashboard')
        else:
            return HttpResponse("<h1>Invalid User!!!!</h1>")
    return render(request, 'myapp/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@doctor_required
def doctor_dashboard(request):
    user = request.user
    context = {'user':user}
    return render(request, 'myapp/doctor_dashboard.html', context)

@login_required(login_url='login')
def patient_dashboard(request):
    if request.user.is_authenticated and request.user.user_type=='doctor':
        return redirect('doctor-dashboard')
    return render(request, 'myapp/patient_dashboard.html')