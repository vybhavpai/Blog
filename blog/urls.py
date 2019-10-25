from django.urls import path
from . import views
from blog.views import(

	create_blog_view,
	detail_blog_view,
	edit_blog_view,
)

app_name = 'blog'

urlpatterns = [
	path('create',create_blog_view, name="create"),
	path('<slug>/',detail_blog_view, name="detail"),
	path('<slug>/edit/',edit_blog_view, name="edit"),
	path('likes/<slug>/',views.blog_like,name="likes"),

]