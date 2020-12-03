import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9486	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

'''
Define variables:
username && passwd
message queue for each user
'''
clients = []
userpass = [ ['user1', 'pass1'], ['user2', 'pass2'], ['user3', 'pass3'] ]
messages = [[],[],[]]
subscriptions = [[],[],[]] # Store the group info

'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn):
	global clients
	global count
	# Tips: Sending message to connected client
	conn.send('Welcome to the server. Please enter your username and password.') #send only takes string
	rcv_msg = conn.recv(1024)
	rcv_msg = stringToTuple(rcv_msg)
	if rcv_msg in userpass:
		user = userpass.index(rcv_msg)
		
		try :
			conn.sendall('valid')
		except socket.error:
			print 'Send failed'
			sys.exit()

		'''
		Part-2: 
		After the user logs in, check the unread message for this user.
		Return the number of unread messages to this user.
		'''
			
		# Tips: Infinite loop so that function do not terminate and thread do not end.
		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				print 'Logout'
				# Logout that you implemented in Part-1
				break
			elif option == str(2):
				print 'Send Message'
				message = conn.recv(1024)
				if message == str(1):
					'''
					Part-2: Send private message
					'''
					print 'Sending private message'
					pmsg = stringToTuple(conn.recv(1024))
					rcv_id = stringToTuple(conn.recv(1024))

					
				if message == str(2):
					'''
					Part-2: Send broadcast message
					'''
					print 'Sending broadcast message'
				if message == str(3):
					'''
					Part-2: Send group message
					'''
					print 'Sending group message'
			elif option == str(3):
				print 'Group configuration'
				'''
				Part-2: Join/Quit group
				'''
			elif option == str(4):
				print 'Offline Messages'
				'''
				Part-2: Read offline message
				'''

			elif option == str(0):
				count = 0
				for x in userpass:
					print(x)
				print 'Popping'
				userpass.pop(1)
				for x in userpass:
					print(x)
				
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats
'''
while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
	elif message == 'listgroup':
		'''
		Part-2: Implement the functionality to list all the available groups
		'''
s.close()
