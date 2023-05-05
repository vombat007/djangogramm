from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.register, name='registration'),
    path('confirm_email/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('profile', views.user_profile, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('profile/edit_profile', views.edit_profile, name='edit_profile'),
    path('profile/change_password', views.change_password, name='change_password'),
    path('create_post', views.create_post, name='create_post'),
    path('post', views.post_page, name='post'),
    path('following/<str:username>/', views.following, name='following'),
    path('following_post', views.following_post, name='following_post'),
    path('like', views.like, name='like'),
]
