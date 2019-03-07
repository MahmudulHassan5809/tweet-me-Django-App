from django.urls import path
from tweets.api import views


app_name = 'user_api'

urlpatterns = [
	path('<username>/tweets/',views.TweetListAPIView.as_view(),name='user_tweet_api'),
]
