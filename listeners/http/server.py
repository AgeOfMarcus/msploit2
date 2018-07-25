#!/usr/bin/python3

from flask import Flask, request

class Listener(object):
	options = {
		'addr':"Server address to listen on",
		'port':"Server port to listen on",
	}
	task = None
	result = None
	app = Flask(__name__)
	@app.route("/",methods=['GET','POST'])
	def serve(self):
		if request.method == "GET":
			if self.task is None:
				return "none",200
			else:
				cmd = self.task
				self.task = None
				return cmd, 200
		elif request.method == "POST":
			data = request.json['result']
			self.result = data
			return "ok", 200
	def sendCommand(self,command,force=False):
		if (not self.task is None) or force:
			self.task = command
			return None
		else:
			return "Failed: Previous command hasn't been completed"
	def run(self,args):
		self.app.run(host=args['addr'],port=int(args['port']))