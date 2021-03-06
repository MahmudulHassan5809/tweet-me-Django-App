"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from accounts.views import UserRegisterView

from django.conf.urls.static import static
from django.conf import settings

from tweets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/',include('tweets.urls')),
    path('', include('django.contrib.auth.urls')),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('api/tweets/',include('tweets.api.urls')),
    path('api/',include('accounts.api.urls')),
    path('tags/',include('hashtags.urls')),
    path('register/',UserRegisterView.as_view(),name='register'),
    path('', views.TweetListView.as_view(),name='home'),

]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
