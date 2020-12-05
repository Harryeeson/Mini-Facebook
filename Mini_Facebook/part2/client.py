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

			if reply == 'Pmsg':
				time.sleep(1)
				reply_pmsg = stringToTuple(s.recv(4096))
				print 'Private message from: ', reply_pmsg[1]
				print reply_pmsg[0]

			elif reply == 'Bmsg':
				time.sleep(1)
				reply_bmsg = s.recv(4096)
				print 'Broadcasted Message: '
				print reply_bmsg

			elif reply == 'Gmsg':
				#time.sleep(1)
				reply_gmsg = stringToTuple(s.recv(4096))
				#time.sleep(1)
				msg_from = stringToTuple(s.recv(4096))
				print msg_from
				print 'Group ', reply_gmsg[0], 'message from: ', msg_from[0]
				print reply_gmsg[1]
			
			elif reply == 'No_grp':
				print 'Cannot send message. You are not in this group.'

			elif reply == 'No_msg':
				print 'No offline messages to read'

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
	s_pms = s.recv(4096)
	'''
	Part-2: Please printout the number of unread message once a new client login
	'''
	print 'You have ', s_pms, ' number of unread private messages'
	s_gms = s.recv(4096)
	print 'You have ', s_gms, ' number of unread group messages'

	start_new_thread(receiveThread, (s,))
	message = ""
	while True :	
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Send messages \n 3. Group Configuration \n 4. Offline message \n")		
		try :
			s.sendall(message)
			if message == str(1):
				print 'Logout'
				break
				
			elif message == str(2):
				print 'Send message'
				while True:
					message = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
					try :
						'''
						Part-2: Send option to server
						'''
						s.sendall(message)

						if message == str(1):
							rcv_id = raw_input("Enter the recevier ID:\n")
							sndr_msg = raw_input("Enter your private message\n")
							pmsg = tupleToString((rcv_id, sndr_msg))

							try :
								'''
								Part-2: Send private message
								'''
								s.sendall(pmsg)
								break
							except socket.error:
								print 'Private message failed to send'
								sys.exit()

						elif message == str(2):
							bmsg = raw_input("Enter your broadcast message\n")
							try :
								'''
								Part-2: Send broadcast message
								'''
								s.sendall(bmsg)
								break
							except socket.error:
								print 'Broadcast Message Send failed'
								sys.exit()
						elif message == str(3):
							g_id = raw_input("Enter the Group:\n")
							gsndr_msg = raw_input("Enter your group message\n")
							gmsg = tupleToString((g_id, gsndr_msg))
							try :
								'''
								Part-2: Send group message
								'''
								s.sendall(gmsg)
								break
							except socket.error:
								print 'Group message failed to send'
								sys.exit()
					except socket.error:
						print 'Message Send failed'
						sys.exit() 
					
			elif message == str(3):
				print 'Group configuration'
				option = raw_input("Do you want to: 1. Join Group 2. Quit Group: \n")
				s.sendall(option)
				if option == str(1):
					group = raw_input("Enter the Group you want to join: ")
					try :
						'''
						Part-2: Join a particular group
						'''
						s.sendall(group)

					except socket.error:
						print 'group info sent failed'
						sys.exit()
				elif option == str(2):
					group = raw_input("Enter the Group you want to quit: ")
					try :
						'''
						Part-2: Quit a particular group
						'''
						s.sendall(group)

					except socket.error:
						print 'group info sent failed'
						sys.exit()
				else:
					print 'Option not valid'
			
			elif message == str(4):
				print 'Offline messages'
				while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
					pass
				option = raw_input("Do you want to: 1. View all offline messages; 2. View only from a particular Group\n")
				s.sendall(option)
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
						s.sendall(group)

					except socket.error:
						print 'group Send failed'
						sys.exit()
				else:
					print 'Option not valid'
	
		except socket.error:
			print 'Send failed'
			sys.exit()
		
else:
	print 'Invalid username or passwword'

s.close()
