from django.contrib import admin
from .models import CustomUser, Category, BlogPost


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(BlogPost)