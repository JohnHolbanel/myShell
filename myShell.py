# Use python3 to run this code
# Student Name: John Laurentiu Holbanel
# Student ID: 17393851

import os
import getpass
import socket
import pathlib
import sys
import readline
from threading import Thread
from subprocess import *

def read_line(USER, HOST, PWD):
	line = input("\n" + USER + " in " + HOST + " at " + PWD + " --> ").strip()
	return line

def io_redirection(args):
	output_file = args[-1]
	if ">>" in args:
		output_file = open(output_file, 'a')		# now appends into output_file
	elif ">" in args:
		output_file = open(output_file, 'w')		# now overwrites the output_file
	if "python3" == args[0]:				# to check if its a file redirection
		if len(args) == 4:					# if there are no arguments
			p = Popen(args[:2], stdin=PIPE, stdout=output_file)
		elif len(args) == 5:				# if there is 1 argument
			p = Popen(args[:3], stdin=PIPE, stdout=output_file)
		elif len(args) == 6:				# if there is 2 arguments
			p = Popen(args[:4], stdin=PIPE, stdout=output_file)
		output = p.communicate()

	else:
		arg = args[:-2]
		execute(arg)

def launch(args):
	pid = os.fork()
	if pid > 0:						# in the parent process
		wpid = os.waitpid(pid, 0)	# Wait for completion of a child process given by process id pid
	else:
		try:
			os.execvp(args[0], args)	# Executes args[0] with argument list args, replacing the current process
		except Exception as e:
			print("myShell: command not found: " + args[0])

def execute(args):
	try:
		if len(args) == 0:			# if user doesnt supply anything just ignore
			pass
		elif "&" == args[-1]:		# if an "&" is found at the end of a command
			background_process = Thread(target=execute, args=(args[:-1],))		# creates a new thread
			background_process.start()				# starts thread
		elif "cd" == args[0]:	
			cd("".join(args[1:]))
		elif "dir" == args[0]:
			dir(args)
		elif "environ" == args[0]:
			environ(args)
		elif "echo" == args[0]:
			echo(args[1:])
		elif "clr" == args[0]:
			clear(args)
		elif "pause" == args[0]:
			pause(args)
		elif "help" == args[0]:
			help(args)
		elif "quit" == args[0]:
			quit(args)
		else:
			launch(args)
	except EOFError as e:
		print("")

def cd(args):
	try:
		if len(args) == 0:			# if cd is only given by user change directory to home_dir
			current_dir = os.getcwd()
			os.chdir(current_dir)
		else:
			os.chdir(args)			# change directory to given path
	except Exception as e:			# if directory doesn't exist print error
		print(e)
		print("cd: no such file or directory: " + args)

def dir(args):
	if len(args) == 1:		# if command is dir with no argument list out all files within the current directory
		for f in os.listdir('.'):		# puts all files into a list
			print(f)
	else:
		try:
			os.chdir(args[1])			# change directory to the one given by the user
			files = [f for f in os.listdir('.')]		# puts all files into a list
			for f in files:
				print(f)
			os.chdir('..')			# change the directory back to where it was before the command was given
		except FileNotFoundError:
			print("Error: Directory not found.")

def environ(args):
	if len(args) == 1:
		for k, v in os.environ.items():		# iterating through the keys and values of the dictionary os.environ
			print(k)
			print(v + "\n")
	else:
		print("Incorrect use of environ command.")

def echo(args):
	print(" ".join(args))		# joins the argument together with spaces between them and prints it

def clear(args):
	if len(args) == 1:
		os.system('clear')		# executing a shell command. In this case it's to "clear" the terminal
	else:
		print("Incorrect use of clr command.")

def pause(args):
	if len(args) == 1:
		print("Paused. Press Enter to continue.")
		input()					# waits for user to press Enter to continue
	else:
		print("Incorrect use of pause command.")

def help(args):
	if len(args) == 1:
		print("\n*use space followed by enter to go through the manual*\n\n")
		with open("readme", "r") as h:		# opens user manual
			lines = h.readlines()
			lines = lines[2:]				# to remove name and student id number from manual
			line_counter = 0
			for line in lines:
				if line_counter == 25:		# if it hits 25 then we will wait for user to input a space to continue
					while True:				# infinite loop waiting for user to use space to continue
						space = input()
						if space == " ":
							line_counter = 0		# resets the line counter
							break					# breaks out of infinte loop and proceeds to continue printing lines
				print(line)
				line_counter += 1			# incrementing line counter everytime a line is printed
	else:
		print("Incorrect use of help command.")

def quit(args):
	if len(args) == 1:
		sys.exit()				# exits the program
	else:
		print("Incorrect use of quit command.")

def main():
	print("Welcome to myShell.")
	if len(sys.argv) == 1:
		while True:
			USER = getpass.getuser()			# returns login name from user
			HOST = socket.gethostname()			# returns the hostname of the machine
			PWD = os.getcwd()					# returns current working directory
			line = read_line(USER, HOST, PWD)	# takes user input
			args = line.split()					# puts input into a list
			if ">" in args or ">>" in args:				# I/O redirection
				if "&" == args[-1]:				# # if an "&" is found at the end of a command
					background_process = Thread(target=io_redirection, args=(args[:-1],))	# creates a new thread
					background_process.start()		# starts thread
				else:
					io_redirection(args)
			else:
				execute(args)
	elif len(sys.argv) == 2:					# this is if user uses a batchfile
		try:
			for line in open(sys.argv[1], "r"):		# opens batchfile and executes the commands within it
				line = line.split()
				if ">" in line or ">>" in line:				# I/O redirection
					io_redirection(line)
				else:
					execute(line)
		except FileNotFoundError:
			print("myShell: cannot access " + sys.argv[1] + ": No such file or directory.")

if __name__ == '__main__':
	main()