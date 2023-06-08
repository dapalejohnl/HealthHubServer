# HealthHubServer

### Starting the server
Start the server by using the command prompt and typing:
```
..\HealthHubServer\server\HealthHub python manage.py runserver
```
Once running, you can use any browser you'd like to test if the local server is running. You can do so by typing:
```
127.0.0.1:8000/
```
and then press enter to see what is returned! If you get a response, it should say "Hello World!"

### Creating test API calls with the "request helper"
You can use HealthHubServer/server/HealthHub/helpers/requesttester.py and its associated "requesttestsettings.json" file to create test calls. Edit the .json file to change the requests. You can then run this to run the file:
```
python reqeusttester.py requesttestsettings.json
```

# Backend APIs
- All APIs besides the first two account endpoints should have the session id as a header:
```
["session-id"] = "abacca-1313a"
```

- All APIs are expecting input and output to be in encoded json

# Error Codes
All APIs have their own error codes, in ADDITION to these error codes that apply to all of them:
```
101: internal error
102: no session id (not logged in / session id not passed as a header)
103: user not authorized
104: incorrect request type (example: GET request when POST request expected)
105: incorrect data input
106: session id expired
```

## **User APIs**

### /users/create [POST]
Attempts to create a new user by email and returns the UID if created
```
Expected data:
{
	email: "aaaa"
	password: "password123"
}
Returned data:
{
	status: {success: True, errorCode: 0},
	userUID: "abc"
}
```
#### Call-specific error codes
```
0: None, successful
1: User with email already exists
```
### /users/login [POST]
Attempts to login a user given their credentials
```
Expected data:
{
	email: "aaaaa",
	password: "aaaa",
}
Returned data:
{
	status: {success: True, errorCode: 0},
	sessionId: "asdkasdjk23j123jkdasd"
}
```
### Call-specific error codes
```
0: None, successful
1: email does not exist
2: password incorrect
```
### /users/logout [GET]
Attempts to login a user given their credentials
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0}
}
```
### /users/logevents [POST]
Attempts to log a health event for a user. This event should only be called internally
```
Expected data: {
	userUID: "aaa",
	events: [
		{type: "HKWalkSpeed", value: 1, startTimestamp: 0, endTimestamp: 1},
		{type: "HKWalkSpeed", value: 1, startTimestamp: 0, endTimestamp: 1},
		{type: "HKWalkSpeed", value: 1, startTimestamp: 0, endTimestamp: 1},
		{type: "HKWalkSpeed", value: 1, startTimestamp: 0, endTimestamp: 1}
	]
}
Returned data:
{
	status: {success: True, errorCode: 0}
}
```
### /users/getevents [GET]
Attempts to get health events for a specific user.
```
Expected data: {
	userUID: "aaa",
	typeName: "HKQuantityTypeIdentifierFlightsClimbed",
	eventCount: 30 #Range between 1-100
}
Returned data:
{
	status: {success: True, errorCode: 0},
	data: [
		{timestamp: 1, value: 1.0},
		{timestamp: 2, value: 2.5},
		{timestamp: 3, value: 4.2},
		{timestamp: 4, value: 1.1}
	]
}
```
### /users/settings/get [GET]
Attempts to get the list of built-in settings for a currently logged in user (session-id)
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	settings: {
		sex: "f",
		weight: 58.4,
		height: 167.8,
		allowedExercises: {
			yoga: true,
			pilates: true,
			cycling: true,
			stretching: true,
			tai chi: true,
			weightlifting: true,
			rowing: true,
			squats: true,
			walking: true,
			running: true,
			hiking: true,
			elliptical: true,
			pushups: true,
			swimming: true,
			dance: true,
			lunges: true,
			boxing: true,
		}
	}
}
```
### /users/settings/edit [POST]
Attempts to change any built-in setting
```
Expected data:
{
	settingName: "aaaa",
	value: DATA [variant]
}
Returned data:
{
	status: {success: True, errorCode: 0}
}
```
#### Call-specific error codes
```
0: None, successful
1: Invalid setting type
```
### /users/getlifescore [GET]
Returns calculated lifestyle score. This factors in the last seven days of activies and how close the user got to their ideal recommended plan per day
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	score: 0.864
}
```
### /users/getplanscore [GET]
Returns the user's previous selected plan and its display score
```
Expected data: {
	typeName: "exercise" #"exercise", "meal", "sleep"
}
Returned data:
{
	status = {}
	scoreNumerator = 114,
	scoreDenominator = 2000,
	plan = {name = "swimming", value = 114},
}
```



## **Recommendation APIs**

### /recommendations/get [GET]
Attempts to get the next set of recommendations
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	exercise: [
		{type = "exercise", name: "swimming", duration: 3600},
		{type = "exercise", name: "running", duration: 1800},
		{type = "exercise", name: "push ups", duration: 600}
	],
	meal: [
		{type = "meal", name: "pasta", calories: 800},
		{type = "meal", name: "fruits", calories: 650},
		{type = "meal", name: "banana", calories: 400}
	],
	sleep: [
		{type = "sleep", duration: 3600},
		{type = "sleep", duration: 1800},
		{type = "sleep", duration: 600}
	]
}
```
### /recommendations/chooseplan [POST]
Attempts to log the user's preference based on recommendations given. This is used to determine lifestyle scores later on
```
Expected data: {
	planName: "exercise",
	idealPlan: {type = "exercise", name: "swimming", duration: 3600},
	chosenPlan: {type = "exercise", name: "running", duration: 1800}
}
Returned data:
{
	status: {success: True, errorCode: 0}
}
```