from django.shortcuts import render,redirect, get_object_or_404
from blog.models import BlogPost, Comment,Likes,Extra_Image, Categories
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm,ImageUpdateForm
from account.models import Account
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import subprocess

# Create your views here.

class Content:

	def __init__(self,content,img=None):
		self.content=content
		self.img=img

def create_blog_view(request):

	context = {}

	user = request.user
	user_id=Account.objects.filter(username=request.user).first()
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	#print(request.POST.get('title'))
		
	
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		category_list_unsplit = form.cleaned_data['category']
		if category_list_unsplit:
			category_list = category_list_unsplit.split(':')
			for category in category_list:
				cat_obj = Categories()
				cat_obj.blog_id = BlogPost.objects.get(title=form.cleaned_data['title'])
				cat_obj.category = category
				cat_obj.save()

		form = CreateBlogPostForm()
		for f in request.FILES.getlist('other_image'):
			img=Extra_Image()
			img.blog_id=obj
			img.image=f
			img.save()

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

		comment_obj.blog_id = blog_post
		
		comment_obj.save()

	context = {}
	
	context['slug']=slug
	blog_post = get_object_or_404(BlogPost, slug=slug)
	img=Extra_Image.objects.filter(blog_id=blog_post)
	context['image_list']=img
	
	user = request.user
	if not user.is_authenticated:
		context['valid_user'] = False
	else:
		context['valid_user'] = True
	

	try:
		like_obj=Likes.objects.get(blog_id=blog_post,user_id=Account.objects.filter(username=request.user).first())
		context['like_status']=True
	except:
		context['like_status']=False

	context['blog_post'] = blog_post
	# print(blog_post.body)
	content=blog_post.body.split('<img>')
	
	category_list = Categories.objects.filter(blog_id = blog_post)
	context['category_list'] = category_list

	content_img=[]
	for i in range(len(img)):
		f=Content(content[i],img[i])
		content_img.append(f)
	context['last_text_body'] = content[-1]

	context['content_img']=content_img
	comments=Comment.objects.filter(blog_id=blog_post)
	context['comments'] = comments
	context['likes']=blog_post.like_count
	context['content']=content
	return render(request,'blog/detail_blog.html',context)

@csrf_exempt
def blog_like(request,slug):
	if request.method=="POST":
		blog_post = get_object_or_404(BlogPost, slug=slug)
		blog_post.like_count+=1
		blog_post.save()
		user_id=Account.objects.filter(username=request.user).first()
		print(blog_post,user_id)
		like=Likes()
		like.blog_id=blog_post
		like.user_id=user_id
		like.save()
		#print(request.POST)

	
	#print(request.data)
	
	return JsonResponse({'name':'Shashank'})

@csrf_exempt
def blog_dislike(request,slug):
	if request.method=="POST":
		blog_post = get_object_or_404(BlogPost, slug=slug)
		blog_post.like_count-=1
		blog_post.save()
		user_id=Account.objects.filter(username=request.user).first()
		like=Likes.objects.get(blog_id=blog_post,user_id=user_id)
		like.delete()

	return JsonResponse({'name':'disliked'})

def edit_blog_view(request,slug):

	context = {}
	print(request.POST)
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost,slug=slug)

	if blog_post.author != user:
		return HttpResponse("you are not the author of this blog post. ")

	img_list = Extra_Image.objects.filter(blog_id=blog_post)
	context['img_list'] = img_list
	
	
	if request.POST:
		print(request.FILES)
		form = UpdateBlogPostForm(request.POST or None,request.FILES or None, instance=blog_post)		
		# formB = ImageUpdateForm()
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	formA = UpdateBlogPostForm(
			initial = {
				"title": blog_post.title,
				"body": blog_post.body,
				"image": blog_post.image,
					
			}
		)
	formB=[]
	for img in img_list:

		form = ImageUpdateForm(
			initial = {
				"image": img_list[0].image,
				# "body": blog_post.body,
				# "image": blog_post.image,
					
			}
		)
		formB.append(form)

	# formB = [ImageUpdateForm(prefix=str(x), instance=Extra_Image()) for x in range(len(img_list))]
	# print(formB[0].initial['image'])

	context['formA'] = formA
	context['formB'] = formB
	context['slug'] = slug

	return render(request,'blog/edit_blog.html',context)

@csrf_exempt
def delete_blog(request, slug):
	if request.method=="POST":
		print(request.POST)
		blog_post = get_object_or_404(BlogPost,slug=slug)
		blog_post.delete()
		print('blog deleted')
		#return JsonResponse({'ab':'ab'})
		return HttpResponseRedirect('/home')


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


