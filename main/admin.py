from django.contrib import admin
from .models import Category, NewsArticle

# A class to control how NewsArticle is displayed in the admin
class NewsArticleAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('title', 'category', 'publication_date')
    # Fields to add a filter sidebar for
    list_filter = ('category', 'publication_date')
    # Fields to search by
    search_fields = ('title', 'content')

# Register your models here.
admin.site.register(Category)
# Register NewsArticle with its custom admin class
admin.site.register(NewsArticle, NewsArticleAdmin)