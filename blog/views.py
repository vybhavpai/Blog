from django.shortcuts import render,redirect, get_object_or_404
from blog.models import BlogPost, Comment, Categories
from django.http import HttpResponse
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from django.db.models import Q
# Create your views here.

def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		category_list = form.cleaned_data['category'].split(':')
		for category in category_list:
			cat_obj = Categories()
			cat_obj.blog_id = BlogPost.objects.get(title=form.cleaned_data['title'])
			cat_obj.category = category
			cat_obj.save()

		form = CreateBlogPostForm()

	context['form'] = form

	return render(request,'blog/create_blog.html',context)

def detail_blog_view(request,slug):

	if request.method=="POST":
		comment=request.POST.get('comment')
		comment_obj = Comment()
		comment_obj.comment_text = comment
		#print(Account.objects.filter(username=request.user).first().username)
		comment_obj.user_id = Account.objects.filter(username=request.user).first()
		
		blog_post = get_object_or_404(BlogPost, slug=slug)
		print(blog_post)
		comment_obj.blog_id = blog_post
		
		comment_obj.save()

	# 	comments=Comment.objects.filter(blog_id=blog_post)

	# 	return render(request,'blog/detail_blog.html',{'comments':comments})


	# else:

	context = {}
	
	context['slug']=slug
	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post
	category_list = Categories.objects.filter(blog_id = blog_post)
	context['category_list'] = category_list
	
	comments=Comment.objects.filter(blog_id=blog_post)
	context['comments'] = comments
	context['likes']=blog_post.like_count
	return render(request,'blog/detail_blog.html',context)

def blog_like(request):

	print(request)

def edit_blog_view(request,slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	if blog_post.author != user:
		return HttpResponse("you are not the author of this blog post. ")
	
	blog_post = get_object_or_404(BlogPost,slug=slug)
	if request.POST:
		form = UpdateBlogPostForm(request.POST or None,request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial = {
				"title": blog_post.title,
				"body": blog_post.body,
				"image": blog_post.image,
					
			}
		)
	context['form'] = form

	return render(request,'blog/edit_blog.html',context)

def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ") #splits vybhav pai to [vybhav, pai]

	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__contains=q) |
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))


