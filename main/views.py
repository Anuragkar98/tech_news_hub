from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login
from .models import NewsArticle, Category, Comment
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from .models import NewsArticle, Favorite
from django.core.paginator import Paginator

# View for the homepage, which will show a list of all recent articles
# main/views.py

def home(request):
    categories = Category.objects.all()
    articles_by_category = {}
    for category in categories:
        # We get all articles for the category to display the section title
        articles_in_category = NewsArticle.objects.filter(category=category).order_by('-publication_date')
        
        # But we only pass the first 4 to the template to keep sections short
        articles_by_category[category] = articles_in_category[:4] 

    context = {
        'articles_by_category': articles_by_category,
        'categories': categories,
    }
    return render(request, 'main/home.html', context)

# View for a specific category page
def category_view(request, category_name):
    category = get_object_or_404(Category, name__iexact=category_name)
    # Get all articles for the category
    all_articles = NewsArticle.objects.filter(category=category).order_by('-publication_date')
    
    # Create a Paginator object
    paginator = Paginator(all_articles, 8) # Show 8 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) # Get the requested page

    categories = Category.objects.all()
    context = {
        'category': category,
        'page_obj': page_obj, # Pass the page object to the template
        'categories': categories,
    }
    return render(request, 'main/category.html', context)

# View for a single news article (the detail page)
def article_detail(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    comments = article.comments.all()
    new_comment = None

    # Check if the logged-in user has favorited this article
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, article=article).exists()

    # Comment posting logic
    if request.method == 'POST':
        # ... (the existing comment form logic remains the same) ...
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    categories = Category.objects.all()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'is_favorited': is_favorited,  # Add this to the context
    }
    return render(request, 'main/detail.html', context)

def search_view(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    
    if query:
        all_articles = NewsArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct().order_by('-publication_date')
    else:
        all_articles = NewsArticle.objects.none()

    # Create a Paginator object
    paginator = Paginator(all_articles, 8) # Show 8 search results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) # Get the requested page

    context = {
        'page_obj': page_obj, # Pass the page object to the template
        'categories': categories,
        'query': query,
    }
    return render(request, 'main/search_results.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # --- Send the notification email ---
            subject = 'Welcome to Tech News Hub!'
            message = f'Hi {user.username}, thank you for registering at Tech News Hub!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            # --- End of email sending code ---

            return redirect('home')
    else:
        # This runs when a user first visits the page (a GET request)
        form = CustomUserCreationForm()
    
    # This part runs for both GET and POST (if form is invalid) requests
    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'registration/signup.html', context)

@login_required
def toggle_favorite_view(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    # Try to get the favorite object for this user and article
    favorite, created = Favorite.objects.get_or_create(user=request.user, article=article)
    
    # If the favorite was just created, it means the user is adding it.
    # If it wasn't created, it means it already existed, so we delete it.
    if not created:
        favorite.delete()
        
    # Redirect back to the article detail page
    return redirect('article_detail', article_id=article.id)

@login_required
def profile_view(request):
    # This is a more direct and reliable way to get the articles
    favorite_articles = NewsArticle.objects.filter(favorite__user=request.user)
    
    categories = Category.objects.all()
    context = {
        'favorite_articles': favorite_articles,
        'categories': categories,
    }
    return render(request, 'main/profile.html', context)
