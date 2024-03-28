from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import BlogPostForm
from .models import BlogPost, Category
from user.decorators import doctor_required, patient_required
from .utils import paginatePosts


def home(request):
    return render(request, 'myapp/home.html')



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


