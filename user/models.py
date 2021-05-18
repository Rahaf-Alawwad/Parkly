from django.db import models
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name,img="",user_type="1",password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            img=img,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password,first_name, last_name,img="#",user_type="0"):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            img=img,
            user_type=user_type,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username        = models.CharField( verbose_name="username", max_length=30, unique=True)
    first_name        = models.CharField( verbose_name="first_name", max_length=30)
    last_name        = models.CharField( verbose_name="last_name", max_length=30)
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    img           = models.TextField(verbose_name="img")
    user_type        = models.CharField( verbose_name="user_type", max_length=2,default="1")

    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    location        = models.CharField(max_length=255, null=True)
    contact_number  = models.CharField(max_length=12, null=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'email','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

