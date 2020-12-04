import socket
import sys
from thread import *
import getpass
import os
import time

'''
Function Definition
'''
def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096) # receive msg from server
			
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit()
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.0.4'
port = 9486
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server
recv_msg = s.recv(1024)
print recv_msg
username = raw_input("Username: \n")
passwd = getpass.getpass("Password: \n")
loginMsg = tupleToString((username, passwd))
s.sendall(loginMsg)

reply = s.recv(5)
if reply == 'valid':
	print 'Username and password valid'
	#ss = s.recv(4096)
	'''
	Part-2: Please printout the number of unread message once a new client login
	'''
	start_new_thread(receiveThread, (s,))
	message = ""
	while True :	
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Send messages \n 3. Group Configuration \n 4. Offline message \n")		
		try :
			s.sendall(message)
			if message == str(1):
				print 'Logout'
				break
				
			if message == str(2):
				print 'Send message'
				while True:
					message = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
					try :
						'''
						Part-2: Send option to server
						'''
						s.sendall(message)
						if message == str(1):
							pmsg = tupleToString(raw_input("Enter your private message\n"))
							try :
								'''
								Part-2: Send private message
								'''
								s.sendall(pmsg)

							except socket.error:
								print 'Private Message Send failed'
								sys.exit()

							rcv_id = tupleToString(raw_input("Enter the recevier ID:\n"))
							try :
								'''
								Part-2: Send private message
								'''
								s.sendall(rcv_id)
								#break
							except socket.error:
								print 'rcv_id Send failed'
								sys.exit()
						if message == str(2):
							bmsg = raw_input("Enter your broadcast message\n")
							try :
								'''
								Part-2: Send broadcast message
								'''
								#break
							except socket.error:
								print 'Broadcast Message Send failed'
								sys.exit()
						if message == str(3):
							gmsg = raw_input("Enter your group message\n")
							try :
								'''
								Part-2: Send group message
								'''
							except socket.error:
								print 'Group Message Send failed'
								sys.exit()
							g_id = raw_input("Enter the Group ID:\n")
							try :
								'''
								Part-2: Send group message
								'''
								#break
							except socket.error:
								print 'g_id Send failed'
								sys.exit()
					except socket.error:
						print 'Message Send failed'
						sys.exit() 
					
			if message == str(3):
				print 'Group configuration'
				option = raw_input("Do you want to: 1. Join Group 2. Quit Group: \n")
				if option == str(1):
					group = raw_input("Enter the Group you want to join: ")
					try :
						'''
						Part-2: Join a particular group
						'''
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				elif option == str(2):
					group = raw_input("Enter the Group you want to quit: ")
					try :
						'''
						Part-2: Quit a particular group
						'''
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				else:
					print 'Option not valid'
			
			if message == str(4):
				print 'Offline messages'
				while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
					pass
				option = raw_input("Do you want to: 1. View all offline messages; 2. View only from a particular Group\n")
				if option == str(1):					
					try :
						'''
						Part-2: View all offline messages
						'''
					except socket.error:
						print 'msg Send failed'
						sys.exit()
				elif option == str(2):
					group = raw_input("Enter the group you want to view the messages from: ")
					try :
						'''
						Part-2: View only from a particular group
						'''
					except socket.error:
						print 'group Send failed'
						sys.exit()
				else:
					print 'Option not valid'
	
			if message == str(0):
				continue
				
		except socket.error:
			print 'Send failed'
			sys.exit()
		
else:
	print 'Invalid username or passwword'

s.close()
