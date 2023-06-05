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
















def chooseplan(request):
	request_status = RequestChecker.checkRequest(request, session=True, method="POST")
	if request_status == 0:
		data = json.loads(request.body.decode("utf-8"))
		if data.get("planName") and data.get("idealPlan") and data.get("chosenPlan"):
			session_id = request.headers["session-id"]
			session_object = Session.objects.get(sessionUID=session_id)
			
			calculated_score = HealthScores.getPlanScoreRatio(session_object.userUID, data.get("idealPlan"), data.get("chosenPlan"))
			
			# Log a new event for this user
			plan_object = PlanEvent(
				userUID = session_object.userUID,
				createdTime = timezone.now().timestamp(),
				type = data.get("planName"),
				score = calculated_score
			)
			plan_object.save()
			return JsonResponse({"status": {"success": True, "errorCode": 0}})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 105}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})