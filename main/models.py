from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only favorite an article once
        unique_together = ('user', 'article')

    def __str__(self):
        return f'{self.user.username} favorites {self.article.title}'

class Comment(models.Model):
    # Link each comment to a specific news article
    article = models.ForeignKey(NewsArticle, related_name='comments', on_delete=models.CASCADE)
    # Link each comment to the user who wrote it
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on'] # Show the oldest comments first

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'