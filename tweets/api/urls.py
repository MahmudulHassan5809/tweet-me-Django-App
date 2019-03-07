from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
	path('',views.TweetListAPIView.as_view(),name='list'),
	path('create/',views.TweetCreateAPIView.as_view(),name='create'),
	path('<pk>/retweet/',views.ReTweetAPIView.as_view(),name='retweet'),
	path('<pk>/like/',views.LikeToggleAPIView.as_view(),name='like'),

]
