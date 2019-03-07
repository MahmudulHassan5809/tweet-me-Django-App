from django.forms.utils import ErrorList
from django import forms

class FormUserNeededMixin(object):
	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
			return super(FormUserNeededMixin,self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['user Must Be Logged In'])
			return self.form_invalid(form)


class UserOwnerMixin(FormUserNeededMixin,object):
	def form_valid(self,form):
		if form.instance.user == self.request.user:
			return super(FormUserNeededMixin,self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(['This User Is Not Allowed To Chnage This Data'])
			return self.form_invalid(form)

