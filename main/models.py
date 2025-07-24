from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    publication_date = models.DateTimeField(default=timezone.now)
    # Using a ForeignKey to link to the Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title