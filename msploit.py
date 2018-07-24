#!/usr/bin/python3

import os

from subprocess import Popen, PIPE as popen, pipe
from termcolor import colored

# Pretty messages
def error(msg): return "%s %s" % (colored("[!]","red"),msg)
def info(msg): return "%s %s" % (colored("[*]","cyan"),msg)

# Validators and checks
def validate_cwd():
	wd = os.getcwd().split("/")
	if not wd[-1].lower() == "msploit2":
		if not "msploit.py" in ls():
			print(error("Please run this from inside msploit2's directory."))
			exit(0)
def all_listeners():
	return ls(dir="./listeners")

# Running commands server-side
def ls(dir="."):
	return bash("ls "+dir).split("\n")
def bash(cmd):
	res = popen(cmd,stdout=pipe,shell=True).communicate()[0]
	try:
		return res.decode()
	except:
		return str(res)