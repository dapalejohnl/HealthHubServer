from django.db import models

class User(models.Model):
	uid = models.CharField("uid", max_length=64)
	createdTime = models.BigIntegerField("time created")
	email = models.CharField("email", max_length=64)
	password = models.CharField("password", max_length=64)

class UserSettings(models.Model):
	userUID = models.CharField("uid", max_length=64)
	sex = models.CharField(max_length=1)
	weight = models.IntegerField()
	height = models.IntegerField()
	exercises = models.JSONField(default=dict)

class Session(models.Model):
	sessionUID = models.CharField("session uid", max_length=64)
	userUID = models.CharField("user uid", max_length=64)
	createdTime = models.BigIntegerField("time created")
	
class HealthEvent(models.Model):
	userUID = models.CharField("uid", max_length=64)
	createdTime = models.BigIntegerField("time created")
	startTime = models.BigIntegerField("time started", null=True, blank=True)
	endTime = models.BigIntegerField("time ended", null=True, blank=True)
	type = models.CharField("record type", max_length=256)
	value = models.FloatField("record value")
	