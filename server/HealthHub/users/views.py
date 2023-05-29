import uuid
import json
import base64
import datetime

from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from users.models import User

from helpers.requesthelper import RequestChecker

def createuser(request):
	request_status = RequestChecker.checkRequest(request, userUIDRequired=False, method="GET")
	if request_status == 0:
		data = request.GET
		if data.get("username") and data.get("password"):
			
			
			return JsonResponse({
				"status": {"success": True, "errorCode": 0},
			})
		else:
			return JsonResponse({"status": {"success": False, "errorCode": 104}})
	else:
		return JsonResponse({"status": {"success": False, "errorCode": request_status}})
	return JsonResponse({"status": {"success": False, "errorCode": 101}})