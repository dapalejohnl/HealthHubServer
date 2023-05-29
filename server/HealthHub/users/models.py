from django.db import models

class User(models.Model):
	uid = models.CharField("uid", max_length=64)
	createdTime = models.BigIntegerField("time created")
	username = models.CharField("email", max_length=64)
	password = models.CharField("password", max_length=64)