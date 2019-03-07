from django.db import models
from django.core.exceptions import ValidationError

def validate_content(value):
	content = value
	if content == '':
		raise ValidationError("Content Cannot Be Empty")
	return value
