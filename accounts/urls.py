from django.urls import path,include
from . import views


app_name = 'accounts'

urlpatterns = [

	path('<username>/profile/',views.UserDetailView.as_view(),name='detail'),
	path('<username>/profile/follow',views.UserFollowView.as_view(),name='follow'),


]
