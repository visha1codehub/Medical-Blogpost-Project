from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import BlogPost



def paginatePosts(request, posts):
    page = request.GET.get('page')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page=1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    ranges = range(1, paginator.num_pages+1)
    
    return posts, ranges