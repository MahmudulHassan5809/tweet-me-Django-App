from django import forms
from django.forms import Textarea

from .models import Tweet

class TweetModelForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ('content',)
        labels = {
            'content' : ''
        }
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control','placeholder':"Your Message"})
        }



    # def clean_content(self,*args,**kwargs):
    # 	content = self.cleaned_data.get("content")
    # 	if content == '':
    # 		raise forms.ValidationError("Content Cannot be Blank")
    # 	return content

