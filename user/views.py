from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import SignUpForm
from .decorators import patient_required



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
    return render(request, 'user/signup.html', context)




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
    return render(request, 'user/login.html')




def logoutUser(request):
    logout(request)
    return redirect('home')



@login_required(login_url='login')
def user_profile(request, pk):
    user = CustomUser.objects.get(id=pk)
    if user != request.user:
        return HttpResponse('You are not allowed here!!')
    context = {'user':user}
    return render(request, 'user/user_profile.html', context)




@login_required(login_url='login')
@patient_required
def doctors_list(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    context = {'doctors':doctors}
    return render(request, 'user/doctors_list.html', context)

