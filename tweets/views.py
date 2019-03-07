from django import forms
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .mixins import FormUserNeededMixin,UserOwnerMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View
from django.http import HttpResponseRedirect


from .forms import TweetModelForm
from .models import Tweet

# Create your views here.

class RetweetView(View):
	def get(self,request,pk,*args,**kwargs):
		tweet = get_object_or_404(Tweet,pk=pk)
		if request.user.is_authenticated:
			new_tweet = Tweet.objects.retweet(request.user,tweet)
			return redirect('home')
		return HttpResponseRedirect(tweet.get_absolute_url())






#create
class TweetCreateView(LoginRequiredMixin,FormUserNeededMixin,CreateView):
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	model = Tweet
	#success_url = '/tweets/create'
	# fields = [
	# 	#'user',
	# 	'content'
	# ]
	login_url = '/admin/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Create Tweet"
		return context


#Update
class TweetUpdateView(LoginRequiredMixin,UserOwnerMixin,UpdateView):
	form = TweetModelForm
	template_name = 'tweets/update_view.html'
	model = Tweet
	fields = ['content']
	#success_url = '/tweets/create'
	login_url = '/admin/'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = context['object']
		return context


#Delete View
class TweetDeleteView(LoginRequiredMixin,UserOwnerMixin,DeleteView):
	model = Tweet
	template_name = 'tweets/delete_confirm.html'
	success_url = reverse_lazy('home')
	login_url = '/admin/'

#retrive
class TweetDeatilView(DetailView):
	template_name = 'tweets/detail_view.html'
	model = Tweet


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = context['object']
		#print(context)
		return context



class TweetListView(ListView):
	template_name = 'tweets/list_view.html'

	def get_queryset(self,*args,**kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q",None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, **kwargs):
		context = super(TweetListView,self).get_context_data(**kwargs)
		context['title'] = 'All Tweets'
		context['create_form'] = TweetModelForm()
		context['create_url'] = reverse_lazy('tweets:create')
		return context


