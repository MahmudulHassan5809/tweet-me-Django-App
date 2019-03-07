import re
from django.db.models.signals import post_save
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .validators import validate_content
from django.urls import reverse
from django.utils import timezone
from hashtags.signals import parsed_hashtags


# Create your models here.

class TweetManager(models.Manager):
	def retweet(self,user,parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj
		qs = self.get_queryset().filter(user=user,parent=og_parent).filter(
			timestamp__year=timezone.now().year,
			timestamp__month=timezone.now().month,
			timestamp__day=timezone.now().day
		)
		if qs.exists():
			return None
		else:
			obj = self.model(
					parent = og_parent,
					user   = user,
					content= parent_obj.content,
				)
			obj.save()
			return obj

	def like_toggle(self,user,tweet_obj):
		if user in tweet_obj.liked.all():
			is_liked = False
			tweet_obj.liked.remove(user)
		else:
			is_liked = True
			tweet_obj.liked.add(user)

		return is_liked




class Tweet(models.Model):
	parent    = models.ForeignKey("self" , blank=True,null=True,on_delete=models.CASCADE)
	user      = models.ForeignKey(User,on_delete=models.CASCADE)
	content   = models.TextField(max_length=140,validators=[validate_content])
	liked     = models.ManyToManyField(User,blank=True,related_name='liked')
	is_reply  = models.BooleanField(verbose_name='Is A Reply?',default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated   = models.DateTimeField(auto_now=True)
	objects   = TweetManager()

	def __str__(self):
		return str(self.content)

	def get_absolute_url(self):
		return reverse("tweets:detail",kwargs={"pk":self.pk})


	# class Meta:
	# 	ordering = ['-timestamp','content']

	# def clean(self,*args,**kwargs):
	# 	content = self.content
	# 	if content == 'xyz':
	# 		raise ValidationError("Content Cannot Be XYZ")
	# 	return super(Tweet,self.clean(*args,**kwargs))



def tweet_save_receiver(sender,instance,created,*args,**kwargs):
	if created and not instance.parent:
		# notify a user
		user_regex = r'@(?P<username>[\w.@+-]+)'
		usernames = re.findall(user_regex, instance.content)
		if usernames:
			print(usernames)
		# send notification to user here.

		hash_regex = r'#(?P<hashtag>[\w\d-]+)'
		hashtags = re.findall(hash_regex, instance.content)
		if hashtags:
			print(hashtags)
		parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
		# send hashtag signal to user here.




post_save.connect(tweet_save_receiver,sender=Tweet)
