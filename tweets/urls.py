from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'tweets'

urlpatterns = [
	path('',RedirectView.as_view(url="/")),
	path('search/',views.TweetListView.as_view(),name='list'),
	path('create/',views.TweetCreateView.as_view(),name='create'),
	path('<pk>/',views.TweetDeatilView.as_view(),name='detail'),
	path('<pk>/retweet/',views.RetweetView.as_view(),name='retweet'),
	path('<pk>/edit/',views.TweetUpdateView.as_view(),name='update'),
	path('<pk>/delete/',views.TweetDeleteView.as_view(),name='delete'),

]
