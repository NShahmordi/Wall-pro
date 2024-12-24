import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.utils.text import slugify
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
    slug = models.SlugField(max_length=200, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

class Category(models.Model):
    category_name = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey('self',
                                on_delete=models.CASCADE, null=True, blank=True,
                                related_name='children')
    def __str__(self):
        return self.category_name

class City(models.Model):
    city_name = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.city_name

class Advertisement(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True, default='default.jpg')
    price = models.IntegerField()
    room = models.OneToOneField('Room', on_delete=models.CASCADE, related_name='advertisement', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='advertisement', on_delete=models.CASCADE)
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
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user1_rooms', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user2_rooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Room between {self.user1} and {self.user2}"

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.room}"
    
@receiver(post_save, sender=Advertisement)
def create_room_for_advertisement(sender, instance, created, **kwargs):
    if created and not instance.room:
        room = Room.objects.create(token=uuid.uuid4())  # Generate a UUID for the token
        instance.room = room
        instance.save()
