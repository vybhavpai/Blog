from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import datetime


def upload_location(instance, filename, **kwargs):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author.id), title=str(instance.title), filename=filename
		)
	return file_path

def upload_images_location(instance, filename, **kwargs):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.blog_id.author.id), title=str(instance.blog_id.title), filename=filename
		)
	return file_path

class BlogPost(models.Model):
	title			= models.CharField(max_length=50, null=False, blank=False)
	body			= models.TextField(max_length=5000, null=False, blank=False)
	image			= models.ImageField(upload_to=upload_location, null=False, blank=False)
	date_published	= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated	= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	like_count      = models.IntegerField(default=0)
	slug			= models.SlugField(blank=True, unique=True)
	category 		= models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.title
	
@receiver(post_delete, sender=BlogPost)
def  submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)

class Comment(models.Model):
	blog_id=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_published	= models.DateTimeField(default=datetime.now(),verbose_name="date commented", blank=True)
	comment_text=models.CharField(max_length=100,blank=True,null=True)

class Likes(models.Model):

	blog_id=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Extra_Image(models.Model):
	blog_id = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	image = models.ImageField(upload_to=upload_images_location, null=False, blank=False)

class Categories(models.Model):

	blog_id=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
	category = models.CharField(max_length=40, null=False, blank=False)
	
	


