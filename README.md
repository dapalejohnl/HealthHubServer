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

### Creating test API calls with the "reqeust
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
## /users/login [POST]
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
## /users/logout [GET]
Attempts to login a user given their credentials
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0}
}
```
### /users/settings/get [GET]
Attempts to get the list of built-in settings for a user
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	settings: {
		sex: "f",
		weight: 130,
		height: 65,
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
## /users/getlifescore [GET]
Returns calculated lifestyle score
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	score: 86.4
}
```
### Call-specific error codes
```
0: None, successful
1: email does not exist
2: password incorrect
```



## **Recommendation APIs**

### /recommendations/exerciseplan [GET]
Attempts to get the next exercise recommendation
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	plan: [
		{exercise: "swimming", duration: 3600},
		{exercise: "running", duration: 1800},
	]
}
```
### /recommendations/mealplan [GET]
Attempts to get the next meal recommendation
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	plan: [
		{meal: "banana", calories: 400},
		{meal: "fruits", calories: 400},
		{meal: "pasta", calories: 800},
	]
}
```
### /recommendations/sleepplan [GET]
Attempts to get the next sleep recommendation
```
Expected data: NONE
Returned data:
{
	status: {success: True, errorCode: 0},
	plan: [
		{sleepStart: 1685170800, sleepEnd: 1685199600, duration: 28800},
	]
}
```

## **Data Pages Retrieval APIs**

### /datapages/retrieve [GET]
Attempts to retrieve stored data information for the currently logged in session.
```
Expected data: {
	fieldName: "walkingDistance",
	pageNum: 0,
	minTimestamp: 0, [OPTIONAL TIMESTAMP]
	maxTimestamp: 0, [OPTIONAL TIMESTAMP]
}
Returned data:
{
	status: {success: True, errorCode: 0},
	data = [
		{timestamp: 0, value: 67.1},
		{timestamp: 1, value: 65.5},
		{timestamp: 2, value: 63.3},
		{timestamp: 3, value: 62.5},
	]
}
```