import requests
import json
import os
import math
import re
import time
import sys

session = requests.Session()

def CreateRequest(settings_file):
	settings = open(settings_file, "r")
	settings_data = json.load(settings)

	url = "{:s}/{:s}".format(settings_data["url"], settings_data["endpoint"])
	request_method = settings_data["requestMethod"]
	session_id = settings_data["sessionId"]
	request_data = settings_data["data"]
	
	settings.close()

	session.headers.update({"session-id": session_id})

	response = None
	if request_method == "GET":
		response = session.get(url, timeout=2, params=request_data)
	else:
		response = session.post(url, request_data, timeout=2)
	
	print("Response code:", response.status_code)
	if response.status_code == 200:
		print(json.loads(response.text))
	print("\n")
	
if __name__ == "__main__":
	
	if len(sys.argv) >= 2:
		settings_file = sys.argv[1]
		if settings_file:
			CreateRequest(settings_file)
			exit(0)
			
	print("incorrect arguments! Expected: [settings.json (.json file name)]")
	exit(0)