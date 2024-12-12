from django.db import models

# our model
from django.db import models
from django.conf import settings

# Our models
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(unique=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.email

class Category(models.Model):
    category_name = models.ForeignKey(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.category 

class City(models.Model):
    city_name = models.ForeignKey(max_length=20, null=True,blank=True)
    def __str__(self):
        return self.city
    
class Advertisement(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=400,null=True, blank=True)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    slug = models.SlugField(max_length=200, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        ralated_name='advertisement',
        on_delete=models.CASCADE,
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    SHIRT_SIZES = (
        #The existence of each ad has three states:
        ('N', 'New'),
        ('as_new', 'as new'), 
        ('U', 'Used'),
    ) 
    #For each ad, the user can select a status->(max_length=1):
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)  
        
    class Meta:
        ordering = ['-created_at']   
        indexes = [
            models.Index(fields=['-title'])
        ]
    
    def __str__(self):
        return self.title    