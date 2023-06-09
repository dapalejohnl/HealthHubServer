import uuid
import json
import base64
import datetime

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from users.models import User, UserSettings, Session, HealthEvent, PlanEvent

from helpers.requesthelper import RequestChecker
from helpers.datahelper import DefaultDataHelper
from helpers.healthscorehelper import HealthScores

def getplans(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="GET")
	if request_status == 0:
		session_id = request.headers["Session-Id"]
		session_object = Session.objects.get(sessionUID=session_id)
		user_id = session_object.userUID
		
		plan_types = ["exercise", "meal", "sleep"]
		plan_multipliers = [1, 0.75, 0.5]
		plans = {"exercise": [], "meal": [], "sleep": []}
		
		for plan_type in plan_types:
			ideal_score = HealthScores.getIdealScore(user_id, plan_type)
			print(plan_type, ideal_score)
			for multiplier in plan_multipliers:
				new_plan = HealthScores.getRecommendationByScore(user_id, plan_type, ideal_score * multiplier)
				plans[plan_type].append(new_plan)
		
		return JsonResponse({
			"status": {"success": True, "errorCode": 0},
			"exercise": plans["exercise"],
			"meal": plans["meal"],
			"sleep": plans["sleep"]
		})
		
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})

def chooseplan(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="POST")
	if request_status == 0:
		data = RequestChecker.getPostData(request)
		if data.get("planName") and data.get("idealPlan") and data.get("chosenPlan"):
			session_id = request.headers["Session-Id"]
			session_object = Session.objects.get(sessionUID=session_id)
			
			score_ratio = HealthScores.getPlanScoreRatio(session_object.userUID, data.get("idealPlan"), data.get("chosenPlan"))
			point_value = HealthScores.getPlanPointValue(session_object.userUID, data.get("chosenPlan"))
			
			# Log a new event for this user
			plan_object = PlanEvent(
				userUID = session_object.userUID,
				createdTime = timezone.now().timestamp(),
				type = data.get("planName"),
				name = data.get("chosenPlan").get("name"),
				progressRatio = score_ratio,
				score = point_value
			)
			plan_object.save()
			return JsonResponse({"status": {"success": True, "errorCode": 0}})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})