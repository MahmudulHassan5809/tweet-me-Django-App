from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
class UserRegisterForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password')
		password2 = forms.CharField(widget=forms.PasswordInput)
		if password1 != password2:
			raise forms.ValidationError("Password Must match")
		return password2

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__icontains=username).exists():
			raise forms.ValidationError("This Username is Taken")
		return username


	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__icontains=email).exists():
			raise forms.ValidationError("This Email is Taken")
		return email

