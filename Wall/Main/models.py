from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db.models.signals import post_delete
from django.dispatch import receiver
import random
import string
import os
import secrets
from unidecode import unidecode



# Custom User Model
class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_("username"), unique=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20)
    slug = models.SlugField(max_length=200, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use unidecode to handle Persian input
            self.slug = slugify(unidecode(self.username))
        super().save(*args, **kwargs)

# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.category_name

# City Model
class City(models.Model):
    city_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.city_name

# Advertisement Model
class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    SHIRT_SIZES = (
        ('N', 'New'),
        ('as_new', 'as new'),
        ('U', 'Used'),
    )
    shirt_size = models.CharField(max_length=6, choices=SHIRT_SIZES, default='N')
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('sold', 'Sold'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title

    def get_images(self):
        return self.images.all() if self.images.exists() else []

    def save(self, *args, **kwargs):
        if not self.slug:
            # Use unidecode to handle Persian input
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

# Advertisement Image Model
class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads_images/')

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

# Room Model
class Room(models.Model):
    token = models.CharField(max_length=50, unique=True, blank=True, null=False)
    user1 = models.ForeignKey(Users, related_name='user1_rooms', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Users, related_name='user2_rooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Room between {self.user1} and {self.user2}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

# Message Model
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.room}"

# Utility Functions
def generate_unique_token():
    while True:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if not Room.objects.filter(token=token).exists():
            return token

# Signal Handlers
@receiver(post_delete, sender=Advertisement)
def delete_advertisement_images(sender, instance, **kwargs):
    for image in instance.images.all():
        image.delete()

# Bookmark Model
class Bookmark(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='bookmarks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'advertisement')