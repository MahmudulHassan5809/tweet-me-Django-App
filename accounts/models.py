from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.

class UserProfileManager(models.Manager):
	use_for_related_fields = True
	def all(self):
		qs = self.get_queryset().all()
		try:
			if self.instance:
				qs = qs.exclude(user=self.instance)
		except:
			pass
		return qs

	def toggle_follow(self,user,to_toogle_user):
		user_profile,created = UserProfile.objects.get_or_create(user=user)
		if to_toogle_user in user_profile.following.all():
			user_profile.following.remove(to_toogle_user)
			added = False
		else:
			user_profile.following.add(to_toogle_user)
			added = True
		return added


	def is_following(self,user,followed_by_user):
		user_profile,created = UserProfile.objects.get_or_create(user=user)
		if created:
			return False
		if followed_by_user in user_profile.following.all():
			return True
		return False


class UserProfile(models.Model):
	user      = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='profile',on_delete=models.CASCADE) #user.profile
	following = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followed_by',blank=True)
	objects = UserProfileManager()
	# user.profile.following --user i follow
	# user.followed_by -- user that follow me -- reverse relation

	def __str__(self):
		return str(self.following.all().count())


	def get_following(self):
		users = self.following.all()
		return users.exclude(username=self.user.username)



def post_save_user_receiver(sender,instance,created,*args,**kwargs):
	if created:
		new_profile = UserProfile.objects.get_or_create(user=instance)


post_save.connect(post_save_user_receiver,settings.AUTH_USER_MODEL)
