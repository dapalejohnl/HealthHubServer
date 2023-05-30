import uuid
import json
import base64
import datetime

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from users.models import User, UserSettings, Session

from helpers.requesthelper import RequestChecker
from helpers.datahelper import DefaultDataHelper

def createuser(request):
	request_status = RequestChecker.checkRequest(request, session=False, method="POST")
	if request_status == 0:
		data = request.POST.dict()
		if data.get("email") and data.get("password"):
			new_email = data["email"]
			new_password = data["password"]
			user_object = None
			try:
				user_object = User.objects.get(email=new_email)
			except:
				user_object = None
			if not user_object:
				user_id = uuid.uuid4()
				
				#User
				user_object = User(
					uid = user_id,
					createdTime = timezone.now().timestamp(),
					email = new_email,
					password = new_password,
				)
				user_object.save()
				
				#User settings
				user_settings_object = UserSettings(
					userUID = user_id,
					sex = "m",
					weight = 0,
					height = 0,
					exercises = DefaultDataHelper.getExerciseData()
				)
				user_settings_object.save()
				
				return JsonResponse({
					"status": {"success": True, "errorCode": 0}
				})
			else:
				return JsonResponse({"status": {"success": False, "errorCode": 1}})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})
	
def login(request):
	request_status = RequestChecker.checkRequest(request, session=False, method="POST")
	if request_status == 0:
		data = request.POST.dict()
		if data.get("email") and data.get("password"):
			new_email = data["email"]
			new_password = data["password"]
			user_object = None
			try:
				user_object = User.objects.get(email=new_email)
			except:
				user_object = None
			if user_object:
				if user_object.password == new_password:
					new_session_id = uuid.uuid4()
					session_object = Session(
						sessionUID = new_session_id,
						userUID = user_object.uid,
						createdTime = timezone.now().timestamp()
					)
					session_object.save()
					return JsonResponse({
						"status": {"success": True, "errorCode": 0},
						"sessionId": new_session_id,
					})
				else:
					return JsonResponse({"status": {"success": False, "errorCode": 2}})
			else:
				return JsonResponse({"status": {"success": False, "errorCode": 1}})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})

def logout(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="GET")
	if request_status == 0:
		session_id = request.headers["session-id"]
		session_object = Session.objects.get(sessionUID=session_id)
		if session_object:
			session_object.delete()
			return JsonResponse({"status": {"success": True, "errorCode": 0}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})
	
