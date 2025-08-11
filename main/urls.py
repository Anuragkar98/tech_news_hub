from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Path for the Home Page
    # URL: /
    path('', views.home, name='home'),

    # Path for Category Pages
    # Example URL: /category/Mobile/
    path('category/<str:category_name>/', views.category_view, name='category_view'),

    # Path for a single Article's Detail Page
    # Example URL: /article/5/
    path('article/<int:article_id>/', views.article_detail, name='article_detail'), 
    path('search/', views.search_view, name='search_view'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('article/<int:article_id>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('profile/', views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)