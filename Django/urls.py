"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from twitter.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='main-page'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_user/', AddUserView.as_view(), name='add-user'),
    path('user/<int:user_id>/', UserView.as_view(), name='user'),
    path('edit_user/', EditUserView.as_view(), name='edit-user'),
    path('tweet/<int:tweet_id>/', TweetView.as_view(), name='tweet'),
    path('add_tweet/', AddTweetView.as_view(), name='add-tweet'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('message/<int:msg_id>/', MessageView.as_view(), name='message'),
    path('send_message/<int:user_id>/', SendMessageView.as_view(), name='send-msg'),
]