from users.models import User, Session
from django.utils import timezone

session_expiration = 2592000 #30 day session expiration

class RequestChecker():
	def checkRequest(request, session=True, method="GET"):
		print(request.headers)
		#Check request information
		if request.method != method:
			return 104
		
		#Check session / account information
		session_id = None
		if session:
			try:
				session_id = request.headers["Session-Id"]
			except:
				return 102
			
			# Now we can get the user with this session id
			session_object = None
			try:
				session_object = Session.objects.get(sessionUID=session_id)
			except:
				session_object = None
			if session_object:
				#Check if session is still valid
				current_time = timezone.now().timestamp()
				created_time = session_object.createdTime
				if current_time > created_time + session_expiration:
					session_object.delete()
					return 105
			else:
				return 102
		return 0