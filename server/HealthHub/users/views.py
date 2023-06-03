import uuid
import json
import base64
import datetime

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from users.models import User, UserSettings, Session, HealthEvent

from helpers.requesthelper import RequestChecker
from helpers.datahelper import DefaultDataHelper

def createuser(request):
	request_status = RequestChecker.checkRequest(request, session=False, method="POST")
	if request_status == 0:
		data = json.loads(request.body.decode("utf-8"))
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
					"status": {"success": True, "errorCode": 0},
					"userUID": user_id
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
		data = json.loads(request.body.decode("utf-8"))
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
	
def logevents(request):
	request_status = RequestChecker.checkRequest(request, session=False, method="POST")
	if request_status == 0:
		data = json.loads(request.body.decode("utf-8"))
		if data.get("userUID") and data.get("events"):
			event_list = data.get("events")
			health_objects = []
			for event in event_list:
				health_event_object = HealthEvent(
					userUID = data.get("userUID"),
					createdTime = timezone.now().timestamp(),
					type = event.get("type"),
					value = event.get("value"),
					startTime = event.get("startTimestamp"),
					endTime = event.get("endTimestamp")
				)
				health_objects.append(health_event_object)
			HealthEvent.objects.bulk_create(health_objects)
			return JsonResponse({"status": {"success": True, "errorCode": 0}})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})
	
def getevents(request):
	request_status = RequestChecker.checkRequest(request, session=False, method="GET")
	if request_status == 0:
		data = json.loads(request.body.decode("utf-8"))
		if data.get("userUID") and data.get("typeName"):
			min_timestamp_str = data.get("minTimestamp")
			max_timestamp_str = data.get("maxTimestamp")
		
			return_data = []
			events = None
			if min_timestamp_str and max_timestamp_str:
				min_timestamp = int(min_timestamp_str)
				max_timestamp = int(max_timestamp_str)
				events = HealthEvent.objects.filter(userUID=data.get("userUID"), type=data.get("typeName"), startTime__range=(min_timestamp, max_timestamp)).order_by("-startTime")
			else:
				events = HealthEvent.objects.filter(userUID=data.get("userUID"), type=data.get("typeName")).order_by("-startTime")
			for i in range(0, len(events)):
				event_object = events[i]
				return_data.append({
					"timestamp": event_object.startTime,
					"value": event_object.value,
				})
			return JsonResponse({
				"status": {"success": True, "errorCode": 0},
				"data": return_data
			})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})