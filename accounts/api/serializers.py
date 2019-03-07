from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.urls import reverse_lazy

User = get_user_model()

class UserDisplaySerializer(serializers.ModelSerializer):
	follwer_count = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields =  ('username','first_name','last_name','follwer_count','url')


	def get_follwer_count(self,obj):
		return 0

	def get_url(self,obj):
		return reverse_lazy("accounts:detail",kwargs={"username":obj.username})