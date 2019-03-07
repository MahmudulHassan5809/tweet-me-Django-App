from django.urls import path
from . import views


app_name = 'hashtags'

urlpatterns = [
	path('<hashtag>/',views.HashTagView.as_view(),name='hashtag'),
]
