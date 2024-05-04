"""
URL configuration for quizapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from accounts.views import *
from django.contrib.auth.views import LoginView
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', register,name="register"),
    path('login/',coustomlogin, name='login'),
    path('login/accounts/profile/', profile, name='profile'),
    path('profile/', profile, name='profile'),
    path('user_page/', user_page, name='user_page'),
    path('add_question/', add_question, name='add_question'),
    path('display-random-question/', display_random_question, name='display_random_question'),
    path('next-random-question/', next_random_question, name='next_random_question'),
    path('handle_submission/',handle_submission,name='handle_submission'),
    path('analyticals/',analyticals, name='analyticals'),
]
