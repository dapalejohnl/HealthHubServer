from users.models import User
from django.utils import timezone

session_expiration = 2592000 #30 day session expiration

class RequestChecker():
	def checkRequest(request, userUIDRequired=True, method="GET"):
		#Check request information
		if request.method != method:
			return 104
		
		#Check session / account information
		user_id = None
		if userUIDRequired:
			try:
				user_id = request.headers["user-id"]
			except:
				return 102
			# Now we can get the user with this user id
			user_object = None
			try:
				user_object = User.objects.get(userUID=user_id)
			except:
				user_object = None
			if not user_object:
				return 102
		return 0