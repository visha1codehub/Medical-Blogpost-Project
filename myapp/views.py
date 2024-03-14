from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from .forms import SignUpForm, BlogPostForm, AppointmentForm
from .models import CustomUser, BlogPost, Category, Appointment
from .decorators import doctor_required, patient_required
from .utils import paginatePosts
from .calendar_api import api_calender


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
    posts = user.blogpost_set.all()
    posts, ranges = paginatePosts(request, posts)
    context = {'user':user, 'posts':posts, 'ranges':ranges}
    return render(request, 'myapp/doctor_blogposts.html', context)




@login_required(login_url='login')
@patient_required
def patient_dashboard(request):
    categories = Category.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = BlogPost.objects.filter(is_draft=False, category__name__icontains=q)
    posts, ranges = paginatePosts(request, posts)

    context = {'posts' : posts, 'categories' : categories, 'q' : q, 'ranges':ranges}
    return render(request, 'myapp/blogpost_list.html', context)




@login_required(login_url='login')
@doctor_required
def create_blogpost(request):
    form = BlogPostForm()
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        button = request.POST['button']
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            if button == 'draft-btn':
                blog.is_draft = True
            blog.save()
            return redirect('doctor-dashboard')
    context = {'form' : form, 'action':'Create'}
    return render(request, 'myapp/blogpost_form.html', context)



@login_required(login_url='login')
def blogpost_detail(request, pk):
    post = BlogPost.objects.get(id=pk)
    context = {'post' : post}
    return render(request, 'myapp/blogpost_detail.html', context)



@login_required(login_url='login')
@doctor_required
def edit_blogpost(request, pk):
    post = BlogPost.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('You are not allowed here!!')
    form = BlogPostForm(instance=post)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        button = request.POST['button']
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.is_draft = True if button == 'draft-btn' else False
            blog.save()
            return redirect('doctor-dashboard')
    context = {'form' : form, 'action':'Edit'}
    return render(request, 'myapp/blogpost_form.html', context)




@login_required(login_url='login')
@doctor_required
def delete_blogpost(request, pk):
    post = BlogPost.objects.get(id=pk)
    if request.user != post.author:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        post.delete()
        return redirect('doctor-dashboard')
    context = {'post':post}
    return render(request, 'myapp/delete_blogpost.html', context)




@login_required(login_url='login')
def user_profile(request, pk):
    user = CustomUser.objects.get(id=pk)
    if user != request.user:
        return HttpResponse('You are not allowed here!!')
    context = {'user':user}
    return render(request, 'myapp/user_profile.html', context)




@login_required(login_url='login')
@patient_required
def doctors_list(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    context = {'doctors':doctors}
    return render(request, 'myapp/doctors_list.html', context)




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
            api_calender.create_event(appointment)
            return redirect('appointment-detail',pk=appointment.id)
    context = {'form':form}
    return render(request, 'myapp/appointment_form.html', context)




@login_required(login_url='login')
def appointment_detail(request, pk):
    appointment = Appointment.objects.get(id=pk)
    context = {'appointment':appointment}
    return render(request, 'myapp/appointment_detail.html', context)




@login_required(login_url='login')
def appointment_list(request):
    user = request.user
    if user.user_type == 'patient':
        appointments = user.appointment_set.all()
    else:
        appointments = user.doc_appointments.all()
    context = {'appointments':appointments}
    return render(request, 'myapp/appointments_list.html', context)