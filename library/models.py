from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=30)

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    publisher = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    book_image = models.ImageField(upload_to='book/cover_images', default='', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Lend_details(models.Model):

    book_status = (
        ('p', 'pending'),
        ('l', 'lent'), 
        ('r', 'returned'))
    book = models.ForeignKey(Book,on_delete = models.CASCADE)
    reader = models.ForeignKey(User,on_delete =models.CASCADE,blank=True,null=True)
    lent_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=1, choices = book_status, blank = True, default = 'p')