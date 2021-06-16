import socket
import time
import threading

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.bind(("", 7001))
listensocket.listen(1)
print ("--- Listening to socket keys at TCP:7001")

last_command = ""

def read_socket_thread():
	global last_command
	while True:
		print ("Awaiting connection...")
		c,a = listensocket.accept()
		print ("Connection from: " + str(a) )
		while True:
			try:
				m,x = c.recvfrom(1024)
				if m:
					first_line = m.decode().split("\n")[0]
					line_elements = first_line.split(",")
					last_command = line_elements[0]
				else:
					break;
			except Exception as e:
				print ("exception: " + str(e))
				pass
		print ("Disconnected")
	print ("Ending thread")


global socket_thread
socket_thread = threading.Thread(target = read_socket_thread, daemon=True)
socket_thread.start()

while True:
	print ("last_command = {}".format(last_command))
	time.sleep(1)

socket_thread.join()
                
