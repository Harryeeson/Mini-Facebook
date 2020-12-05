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
# messages in format [receiver, msg, sender]
messages = []
# group messages in format [group #, receiver, msg, sender]
grp_messages = []
subscriptions = [ ['user1', 'user2'], ['user2', 'user3'], ['user3', 'user1'] ] # Store the group info

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
		username = rcv_msg[0]
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
		num_pmsg = 0
		num_gmsg = 0
		for x in messages:
			if username == x[0]:
				num_pmsg += 1
		conn.sendall(str(num_pmsg))
		time.sleep(1)
		for y in grp_messages:
			if username == grp_messages[1]:
				num_gmsg += 1
		conn.sendall(str(num_gmsg))
			
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
					pmsg = stringToTuple(conn.recv(1024))   # (rcv_id, sndr_msg)
					online = False
					if pmsg[0] == 'user1':
						for x in clients:
							peer = x.getpeername()
							if peer[0] == '10.0.0.1':
								online = True
								break

						if online:
							x.sendall('Pmsg')
							x.sendall(tupleToString((pmsg[1], username)))

						else:
							messages.append(str([pmsg[0], pmsg[1], username]))

					elif pmsg[0] == 'user2':
						for x in clients:
							peer = x.getpeername()
							if peer[0] == '10.0.0.2':
								online = True
								break

						if online:
							x.sendall('Pmsg')
							x.sendall(tupleToString((pmsg[1], username)))

						else:
							messages.append(str([pmsg[0], pmsg[1], username]))

					elif pmsg[0] == 'user3':
						for x in clients:
							peer = x.getpeername()
							if peer[0] == '10.0.0.3':
								online = True
								break

						if online:
							x.sendall('Pmsg')
							x.sendall(tupleToString((pmsg[1], username)))

						else:
							messages.append(str([pmsg[0], pmsg[1], username]))

					else:
						print 'Incorrect user'
					
				elif message == str(2):
					'''
					Part-2: Send broadcast message
					'''
					print 'Sending broadcast message'
					bmsg = conn.recv(1024)
					for x in clients:
						x.sendall('Bmsg')
						x.sendall(bmsg)

				elif message == str(3):
					'''
					Part-2: Send group message
					'''
					print 'Sending group message'
					gmsg = stringToTuple(conn.recv(1024))
					g_id = int(gmsg[0])
					g_id -= 1
					in_group = False
					for z in subscriptions[g_id]:
						if z == username:
							in_group = True
					if in_group:
						for x in subscriptions[g_id]: 	# names of people in group
							for y in clients:			# connected clients
								online = False
								peer = y.getpeername()
								if conn.getpeername() == peer:
									continue
								if peer[0] == '10.0.0.1':
									online = True

								elif peer[0] == '10.0.0.2':
									online = True

								elif peer[0] == '10.0.0.3':
									online = True

								if online:
									y.sendall('Gmsg')
									time.sleep(1)
									y.sendall(tupleToString((gmsg[0], gmsg[1])))
									time.sleep(1)
									y.sendall(tupleToString((username, 'foo')))
								else:
									grp_messages.append(str(gmsg[0], x, gmsg[1], username))
					else:
						conn.sendall('No_grp')
		
			elif option == str(3):
				print 'Group configuration'
				'''
				Part-2: Join/Quit group
				'''
				message = conn.recv(1024)
				if message == str(1):
					print 'Join group'
					grp = int(conn.recv(1024))
					grp -= 1
					subscriptions[grp].append(username)

				elif message == str(2):
					print 'Quit group'
					grp = int(conn.recv(1024))
					grp -= 1
					lctUser = subscriptions[grp].index(username)
					subscriptions[grp].pop(lctUser)

			elif option == str(4):
				print 'Offline Messages'
				'''
				Part-2: Read offline message
				'''
				message = conn.recv(1024)
				no_msg = True
				if message == str(1): # messages in format [receiver, msg, sender]
					print 'View all offline messages'
					for x in messages:
						if x[0] == username:
							no_msg = False
							conn.sendall('Pmsg')
							conn.sendall(tupleToString((x[1], x[2])))
					if no_msg:
						conn.sendall('No_msg')

				elif message == str(2): # group messages in format [group #, receiver, msg, sender]
					print 'View only from a particular group'
					grp = conn.recv(1024)
					for x in grp_messages:
						if x[0] == grp and x[1] == username:
							no_msg = False
							conn.sendall('Gmsg')
							conn.sendall(tupleToString((x[0], x[2], x[3])))
					
					if no_msg:
						conn.sendall('No_msg')

				
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
		grp_cntr = 1
		for x in subscriptions:
			print 'Group ', grp_cntr
			print x
			grp_cntr += 1

s.close()
