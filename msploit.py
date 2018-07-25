#!/usr/bin/python3

import os, code, sys

from subprocess import Popen as popen, PIPE as pipe
from termcolor import colored

import libs.console as console

# Config
class Vars(object):
	listeners = {}
	agents = {}
	currentListener = None
cfg = Vars()

# Pretty messages
def error(msg): return "%s %s" % (colored("[!]","red"),msg)
def info(msg): return "%s %s" % (colored("[*]","cyan"),msg)
def good(msg): return "%s %s" % (colored("[+]","green"),msg)

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
	res = bash("ls "+dir).split("\n")
	res.remove(res[-1])
	return res
def bash(cmd):
	res = popen(cmd,stdout=pipe,shell=True).communicate()[0]
	try:
		return res.decode()
	except:
		return str(res)

# Loading and using listeners
def load_listener(name,nick=None):
	if not name in all_listeners():
		print(error("Listener does not exist"))
		return False
	if nick is None: nick = name
	if nick in cfg.listeners:
		print(error("Listener nickname is taken"))
		return False
	try:
		exec("import listeners.%s.server as %s" % (name,nick))
		cfg.listeners[nick] = eval(nick).Listener()
		return cfg.listeners[nick]
	except Exception as e:
		print(error("Error importing listener: " + str(e)))
		return False
def print_options(options):
	for i in options:
		print(colored(i,"green") + " : " + colored(options[i],"cyan"))

# Commands menu
man = {
	'help':'Prints the help menu',
	'exit':'Exits the program',
	'uselistener':"Use a listener. Usage: 'uselistener [listener] {nickname}'",
	'show':"Displays something. Usage: 'show [thing]'. Valid arguments: options,listeners",
}
def print_help():
	print(colored("Key","cyan") + ": [] = required argument, {} = optional argument.")
	for i in man:
		print(colored(i,"green") + colored(" : ","cyan") + man[i])
class CmdHandler(object):
	commands = []
	for i in man:
		commands.append(i)
	def handle(self,cmd):
		if ' ' in cmd:
			base = cmd.split(" ")[0]
		else:
			base = cmd
		if base == "help":
			print_help()
		elif base == "exit":
			# exit_sequence()
			return "exit"
		elif base == "uselistener":
			listener = cmd.split(" ")[1]
			if len(cmd.split(" ")) == 3:
				nick = cmd.split(" ")[2]
			else:
				nick = listener
			useless = load_listener(listener,nick=nick)
			if useless:
				print(good("Loaded listener %s as '%s'" % (listener,nick)))
				cfg.currentListener = nick
		elif base == "show":
			try:
				thing = cmd.split(" ")[1]
				if thing == "listeners":
					res = 'Listeners: '
					for i in all_listeners():
						res += colored(i,"green") + ", "
					print(res)
				elif thing == "options":
					if cfg.currentListener is None:
						print(error("No listener is selected"))
					else:
						opt = cfg.listeners[cfg.currentListener].options
						print_options(opt)
			except:
				print(error("Needed argument: [thing]"))
		else:
			print(error("Invalid command"))



# Main program
def start_sequence():
	validate_cwd()
def exit_sequence():
	pass
def handle_args(args):
	pass
def main(args={}):
	if not args == {}:
		handle_args(args)
	start_sequence()
	console.start_shell(CmdHandler())
	exit_sequence()
if __name__ == "__main__":
	if len(sys.argv) == 1:
		main()
	else:
		args = sys.argv; args.remove(args[0])
		main(args=args)