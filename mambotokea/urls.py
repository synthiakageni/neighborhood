from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.home, name='home'),
    path('hood/<int:pk>/', views.hood, name='hood'), 
    path('profile/<int:pk>/', views.userProfile, name='user_profile'),
    path('create_hood/', views.createHood, name='create_hood'),
    path('update_hood/<int:pk>/', views.updateHood, name='update_hood'),
    path('delete_hood/<int:pk>/', views.deleteHood, name='delete_hood'),
    path('delete_post/<int:pk>/', views.deletePost, name='delete_post'),
    path('join_hood/<int:pk>/', views.joinHood, name='join_hood'),
    path('quit_hood/<int:pk>/', views.quitHood, name='quit_hood'),
    path('update_user/', views.updateUser, name='update_user'),
    path('create_business/<int:pk>/', views.createBusiness, name='create_business')
    
]