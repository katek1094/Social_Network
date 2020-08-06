from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome_page, name="welcome_page"),
    path('app/profile/<int:id>/', views.profile_page, name='profile'),
    path('app/wall', views.wall, name="wall"),
    path('app/settings', views.settings, name="settings"),
    path('app/search', views.search, name="search"),
    path('app/friend_requests', views.friend_requests, name="friend_requests"),





]









