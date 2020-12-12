from django.urls import path
from . import views

urlpatterns = [
    path('postcomment/', views.postcomment, name='postcomment'),
    path('profilePic/', views.profilePic, name='profilePic'),
    path('', views.index, name='index'),
    path('readfull/<str:slug>/', views.readfull, name='readfull'),
    path('profile/', views.profile, name='profile'),
    path('dltcomment/<str:sno>/', views.dltcomment, name='dltcomment'),
    path('signup/', views.signup, name='signup'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('postArticle/', views.postArticle, name='postArticle'),
]
