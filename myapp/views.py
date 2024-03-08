from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from .forms import SignUpForm, BlogPostForm
from .models import CustomUser, BlogPost, Category
from .decorators import doctor_required
from .utils import paginatePosts


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
    posts = user.blogpost_set.all()
    posts, ranges = paginatePosts(request, posts)
    context = {'user':user, 'posts':posts, 'ranges':ranges}
    return render(request, 'myapp/doctor_blogposts.html', context)

@login_required(login_url='login')
def patient_dashboard(request):
    if request.user.is_authenticated and request.user.user_type=='doctor':
        return redirect('doctor-dashboard')
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