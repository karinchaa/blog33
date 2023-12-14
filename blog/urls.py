from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, contact, subscription_success, profile, update_profile

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:id>', views.post, name='post'),
    path('services', views.services, name='services'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('category/<str:name>', views.category, name='category'),
    path('search', views.search, name='search'),
    path('create', views.create, name="create"),
    path('login', LoginView.as_view(), name="blog_login"),
    path('logout', LogoutView.as_view(), name="blog_logout"),
    path('register/', register, name='register'),
    path('subscription-success/', subscription_success, name='subscription_success'),
    path('user_profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
]
