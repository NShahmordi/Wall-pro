from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager,TokenGenerator
# Our models
class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_("username"),unique=True,max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20)
    slug = models.SlugField(max_length=200, unique=True,default=username)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
class Category(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.name

class Advertisement(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    slug = models.SlugField(max_length=200, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='advertisement',
        on_delete=models.CASCADE,
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    SHIRT_SIZES = (
        ('N', 'New'),
        ('as_new', 'as new'), 
        ('U', 'Used'),
    )
    shirt_size = models.CharField(max_length=6, choices=SHIRT_SIZES)  
        
    class Meta:
        ordering = ['-created_at']   
        indexes = [
            models.Index(fields=['-title'])
        ]
    
    def __str__(self):
        return self.title

class Room(models.Model):
    token = models.CharField(max_length=255, unique=True)
    users = Users()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = TokenGenerator(20)
        return super(Room, self).save(*args, **kwargs)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="sender_user"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.username