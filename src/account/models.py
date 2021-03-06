from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password = None):		#all the mandatory fields should be taken as input
		if not email:
			raise ValueError('User must have an email address')
		if not username:
			raise ValueError('User must have a username')
		
		user = self.model(
			email =self.normalize_email(email),
			username = username,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email =self.normalize_email(email), 
			password = password,
			username = username, 
			)
		user.is_admin = True
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user



class Account(AbstractBaseUser):
	email					= models.EmailField(verbose_name = "email", max_length = 60,unique = True)
	username				= models.CharField(max_length = 30,unique = True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	first_name				= models.CharField(verbose_name = "first name", max_length = 20,null=False,default="")
	last_name				= models.CharField(verbose_name = "last name", max_length = 20,null=False,default="")
	address					= models.CharField(verbose_name = "address", max_length = 20,null=False,default="")
	phone					= models.CharField(verbose_name = "phone", max_length = 10,null=False,default="")
	
	

	USERNAME_FIELD = 'email' 				#is indicative of what the login id parameter is
	REQUIRED_FIELDS = ['username']			#fields mandatory for the signup

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

