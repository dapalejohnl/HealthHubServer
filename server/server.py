# Extend the path.
import sys
sys.path.append("..")

# Other import statements
from threading import Thread
import random
import collections
import tornado.ioloop
import tornado.web
import requests
import subprocess
import json
import shelve
import time
import asyncio
import tornado.gen as gen
import os
import math
import re
import data_process.data_processing as dp

session = requests.Session()

def ostime():
	return math.floor(time.time())

class HelloWorldHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello World!")

class CodeInputTestHandler(tornado.web.RequestHandler):
	def get(self, code):
		self.write("Code input: " + code)

async def UpdateLoop():
	print("i am a function loop that can do something in the future maybe if we want")
	# Maybe we'd need to do some index iteration at some interval of time?

def make_app():
	return tornado.web.Application([
		(r"/", HelloWorldHandler),
		(r"/([0-9_A-Za-z\-]+)", CodeInputTestHandler),
	])
	
if __name__ == "__main__":
	app = make_app()
	port_num = 80
	address_ip = '127.0.0.1'
	server = tornado.httpserver.HTTPServer(app, no_keep_alive = True)
	server.listen(port_num, address = address_ip)
#tornado.ioloop.IOLoop.current().spawn_callback(UpdateLoop)
tornado.ioloop.IOLoop.current().start()
