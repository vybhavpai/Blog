from django.contrib import admin

from blog.models import BlogPost, Comment, Categories
# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Categories)
