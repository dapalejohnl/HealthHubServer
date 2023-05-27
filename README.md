# HealthHubServer

Start the server by using the command prompt and typing
```
C:\Users\Usr\Directory Python3 server.py
```

Once running, you can use any browser you'd like to test if the local server is running. You can do so by typing:
```
127.0.0.1/
```
and then press enter to see what is returned! If you get a response, it should say "Hello World!"


# Backend APIs
- All APIs besides the first two account endpoints should have the session id as a header:
```
["user-id"] = "abacca-1313a"
```

- All APIs are expecting input and output to be in encoded json

# Error Codes
All APIs have their own error codes, in ADDITION to these error codes that apply to all of them:
```
101: internal error
102: no user id (user id not passed as a header)
103: user not authorized
104: incorrect request type (example: GET request when POST request expected)
105: incorrect data input
```

## **User Settings APIs**

### /settings/get [GET]
Attempts to get the list of built-in settings for a user
```
Expected data: NONE
Returned data:
{
	status: {success = True, errorCode = 0},
	settings: {
		"sex": "f",
		"weight": 130,
		"height": 65,
		"allowedExercises": {
			"yoga": true,
			"pilates": true,
			"cycling": true,
			"stretching": true,
			"tai chi": true,
			"weightlifting": true,
			"rowing": true,
			"squats": true,
			"walking": true,
			"running": true,
			"hiking": true,
			"elliptical": true,
			"pushups": true,
			"swimming": true,
			"dance": true,
			"lunges": true,
			"boxing": true,
		}
	}
}
```

### /settings/change [POST]
Attempts to change any built-in setting
```
Expected data:
{
	settingName: "aaaa",
	value: DATA [variant]
}
Returned data:
{
	status: {success = True, errorCode = 0},
	name: "Plaza Verde Group A",
	userUIDs: [UID1, UID2, UID3],
	propertyUIDs: [UID1, UID2, UID3]
}
```
#### Call-specific error codes
```
0: None, successful
1: Invalid setting type
```


## **Recommendation APIs**

### /recommendations/exerciseplan [GET]
Attempts to get the next exercise recommendation
```
Expected data: NONE
Returned data:
{
	status: {success = True, errorCode = 0},
	plan: [
		{exercise = "swimming", duration = 3600},
		{exercise = "running", duration = 1800},
	]
}
```
### /recommendations/mealplan [GET]
Attempts to get the next meal recommendation
```
Expected data: NONE
Returned data:
{
	status: {success = True, errorCode = 0},
	plan: [
		{meal = "banana", calories = 400},
		{meal = "fruits", calories = 400},
		{meal = "pasta", calories = 800},
	]
}
```
### /recommendations/sleepplan [GET]
Attempts to get the next sleep recommendation
```
Expected data: NONE
Returned data:
{
	status: {success = True, errorCode = 0},
	plan: [
		{sleepStart = 1685170800, sleepEnd = 1685199600, duration = 28800},
	]
}
```