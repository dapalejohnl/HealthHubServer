import uuid
import json
import base64
import datetime

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from users.models import User, UserSettings, Session, HealthEvent, PlanEvent

from helpers.requesthelper import RequestChecker
from helpers.datahelper import DefaultDataHelper

def clamp(n, min_n, max_n):
	return max(min(n, max_n), min_n)

def createuser(request):
	request_status = RequestChecker.checkRequest(request, session=False, method="POST")
	if request_status == 0:
		data = RequestChecker.getPostData(request)
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
					weight = 0.01,
					height = 0.01,
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
		data = RequestChecker.getPostData(request)
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
						"userId": user_object.uid,
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
		session_id = request.headers["Session-Id"]
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
		data = RequestChecker.getPostData(request)
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
		data = request.GET.dict()
		if data.get("userUID") and data.get("typeName") and data.get("eventCount"):
			return_data = []
			
			event_count = clamp(int(data.get("eventCount")), 1, 100)
			events = HealthEvent.objects.filter(userUID=data.get("userUID"), type=data.get("typeName")).order_by("-startTime")[:event_count]
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
	
def getsettings(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="GET")
	if request_status == 0:
		session_id = request.headers["Session-Id"]
		session_object = Session.objects.get(sessionUID=session_id)
		settings_object = UserSettings.objects.get(userUID=session_object.userUID)
		
		return JsonResponse({
			"status": {"success": True, "errorCode": 0},
			"settings": {
				"sex": settings_object.sex,
				"weight": settings_object.weight,
				"height": settings_object.height,
				"allowedExercises": settings_object.exercises,
			}
		})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})
	
def editsettings(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="POST")
	if request_status == 0:
		data = RequestChecker.getPostData(request)
		if data.get("settingName") and data.get("value"):
			session_id = request.headers["Session-Id"]
			session_object = Session.objects.get(sessionUID=session_id)
			settings_object = UserSettings.objects.get(userUID=session_object.userUID)
			
			try:
				attr_val = getattr(settings_object, data.get("settingName"), None)
				if attr_val != None:
					setattr(settings_object, data.get("settingName"), data.get("value"))
					settings_object.save()
			except:
				return JsonResponse({"status": {"success": False, "errorCode": 1}})
			
			return JsonResponse({"status": {"success": True, "errorCode": 0}})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})
	
def getlifescore(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="GET")
	if request_status == 0:
		session_id = request.headers["Session-Id"]
		session_object = Session.objects.get(sessionUID=session_id)
		
		days_considered = 7
		event_types_considered = 0
		total_score = 0
		
		exercise_events = PlanEvent.objects.filter(userUID=session_object.userUID, type="exercise").order_by("-createdTime")[:days_considered]
		meal_events = PlanEvent.objects.filter(userUID=session_object.userUID, type="meal").order_by("-createdTime")[:days_considered]
		sleep_events = PlanEvent.objects.filter(userUID=session_object.userUID, type="sleep").order_by("-createdTime")[:days_considered]
		
		# Exercise score
		if len(exercise_events) > 0:
			event_sum = 0
			for event in exercise_events:
				event_sum += event.progressRatio
			total_score += event_sum / len(exercise_events)
			event_types_considered += 1
		
		# Meal score
		if len(meal_events) > 0:
			event_sum = 0
			for event in meal_events:
				event_sum += event.progressRatio
			total_score += event_sum / len(meal_events)
			event_types_considered += 1
		
		# Sleep score
		if len(sleep_events) > 0:
			event_sum = 0
			for event in sleep_events:
				event_sum += event.progressRatio
			total_score += event_sum / len(sleep_events)
			event_types_considered += 1
		
		averaged_score = 0
		if event_types_considered > 0:
			averaged_score = round(total_score / event_types_considered, 2)
		
		return JsonResponse({
			"status": {"success": True, "errorCode": 0},
			"score": averaged_score,
		})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})

def getplanscore(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="GET")
	if request_status == 0:
		data = request.GET.dict()
		if data.get("typeName"):
			session_id = request.headers["Session-Id"]
			session_object = Session.objects.get(sessionUID=session_id)
			
			days_considered = 1
			score_num = 0
			score_denom = 0
			plan_data = {}
			events = PlanEvent.objects.filter(userUID=session_object.userUID, type=data.get("typeName")).order_by("-createdTime")[:days_considered]
			
			if len(events) > 0:
				plan_event = events[0]
				score_num = int(plan_event.score)
				score_denom = int(plan_event.score * plan_event.progressRatio)
				plan_data = {"name": plan_event.name, "value": int(plan_event.score)}
			
			return JsonResponse({
				"status": {"success": True, "errorCode": 0},
				"scoreNumerator": score_num,
				"scoreDenominator": score_denom,
				"plan": plan_data,
			})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})