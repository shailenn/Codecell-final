"""Codecell URL Configuration

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
from django.urls import path,include,re_path
from Accounts import views,urls
from Quiz import urls as Quiz_urls
from Forum import urls as Forum_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),  # home page 
    path('accounts/',include(urls.registerpatterns)),  # other log in log out tags
    path('quiz/', include(Quiz_urls.Quiz_url_patterns)), # urls in quiz category
    path('forum/', include(Forum_urls.Forum_url_patterns)), # urls in forums
    re_path(r'^(?P<username>[\w|W-]+)/$', views.User_profile.as_view() , name = "user_profile"),
    re_path(r'^(?P<username>[\w|W-]+)/update/$', views.User_update.as_view() , name = "profile_update"),
]
