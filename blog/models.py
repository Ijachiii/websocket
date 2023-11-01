from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, related_name="author", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    sender = models.CharField(max_length=256)
    message = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender}: {self.message}"