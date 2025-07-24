from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)