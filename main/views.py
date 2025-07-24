from django.shortcuts import render
from .models import NewsArticle, Category
from django.db.models import Q

# View for the homepage, which will show a list of all recent articles
# main/views.py

def home(request):
    # Get all categories
    categories = Category.objects.all()
    
    # Create a dictionary to hold the latest 4 articles for each category
    articles_by_category = {}
    for category in categories:
        articles_by_category[category] = NewsArticle.objects.filter(category=category).order_by('-publication_date')[:4]

    context = {
        'articles_by_category': articles_by_category,
        'categories': categories, # Still needed for the navbar
    }
    return render(request, 'main/home.html', context)

# View for a specific category page
def category_view(request, category_name):
    # Get the category object that matches the name
    category = Category.objects.get(name__iexact=category_name)
    # Get all articles belonging to that category
    articles = NewsArticle.objects.filter(category=category).order_by('-publication_date')
    categories = Category.objects.all()
    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'main/category.html', context)

# View for a single news article (the detail page)
def article_detail(request, article_id):
    article = NewsArticle.objects.get(id=article_id)
    categories = Category.objects.all()
    context = {
        'article': article,
        'categories': categories,
    }
    return render(request, 'main/detail.html', context)

def search_view(request):
    query = request.GET.get('q', '') # Get the search query from the URL parameter 'q'
    categories = Category.objects.all()
    
    if query:
        # Search for the query in both the title and content fields
        articles = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        articles = NewsArticle.objects.none() # Return no articles if the query is empty

    context = {
        'articles': articles,
        'categories': categories,
        'query': query,
    }
    return render(request, 'main/search_results.html', context)