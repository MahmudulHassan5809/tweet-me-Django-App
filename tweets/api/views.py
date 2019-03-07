from rest_framework import generics
from .serializers import TweetModelSerializer
from tweets.models import Tweet
from django.db.models import Q
from rest_framework import permissions
from .pagination import StandardResultsSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response


class ReTweetAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self,request,pk,format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not Allowed"
		if tweet_qs.exists() and tweet_qs.count() == 1:
			if request.user.is_authenticated:
				new_tweet = Tweet.objects.retweet(request.user,tweet_qs.first())
				if new_tweet is not None:
					data = TweetModelSerializer(new_tweet).data
					return Response(data)
				message = 'CanNot ReTweet'
			return Response({"message":message},status=400)



class LikeToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self,request,pk,format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not Allowed"
		if request.user.is_authenticated:
			is_liked = Tweet.objects.like_toggle(request.user,tweet_qs.first())
			return Response({"liked":is_liked})

		return Response({"message":message},status=400)


class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self,serializer):
		serializer.save(user = self.request.user)


class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsSetPagination

	# def get_queryset(self):
	# 	return Tweet.objects.all()

	def get_serilazier_context(self):
		context = super(TweetListAPIView,self).get_serializer_context(*args,**kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self,*args,**kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			qs =  Tweet.objects.filter(user__username=requested_user).order_by('-timestamp')
			query = self.request.GET.get("q",None)
			if query is not None:
				qs = qs.filter(
					Q(content__icontains=query) |
					Q(user__username__icontains=query)
					)
			return qs
		else:
			im_following = self.request.user.profile.get_following()
			qs1 = Tweet.objects.filter(user__in=im_following).order_by('-timestamp')
			qs2 =  Tweet.objects.filter(user=self.request.user).order_by('-timestamp')
			qs = (qs1 | qs2).distinct()
			query = self.request.GET.get("q",None)
			if query is not None:
				qs = qs.filter(
					Q(content__icontains=query) |
					Q(user__username__icontains=query)
					)
			return qs
