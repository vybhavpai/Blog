from django.contrib import admin

from blog.models import BlogPost, Comment,Likes,Extra_Image, Categories
# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Extra_Image)
admin.site.register(Categories)
