from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('favorites/toggle/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('history/', views.history_list, name='history'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
]