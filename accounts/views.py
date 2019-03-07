from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views import View
from django.views.generic.edit import FormView
from .forms import UserRegisterForm

from .models import UserProfile

# Create your views here.

class UserRegisterView(FormView):
	template_name = 'accounts/user_register_form.html'
	form_class = UserRegisterForm
	success_url = '/login'

	def form_valid(self, form):
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		newuser = User.objects.create(username=username,email=email)
		newuser.set_password(password)
		new_user.save()
		return super(UserRegisterForm,self).form_valid(form)


class UserDetailView(DetailView):
	model = User
	template_name = 'accounts/user_detail.html'

	def get_context_data(self, **kwargs):
		context = super(UserDetailView,self).get_context_data(**kwargs)
		context['following'] = UserProfile.objects.is_following(self.request.user,self.get_object())
		context['title'] = context['object']
		return context

	def get_object(self):
		return get_object_or_404(User,username__iexact=self.kwargs.get("username"))



class UserFollowView(View):
	def get(self,request,username,*args,**kwargs):
		toggle_user = get_object_or_404(User,username__iexact=username)
		if request.user.is_authenticated:
			is_following = UserProfile.objects.toggle_follow(request.user,toggle_user)
		return redirect('accounts:detail',username=username)
