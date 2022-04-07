import socket
from threading import Thread

def send_server(server):
	while True:
		msg = str(input("> "))
		data = msg.encode('utf-8')
		server.sendall(data)
		print(f"Envoyé : {msg}")

def recv_server(server):
	while True:
		in_data = server.recv(1024)
		in_msg = in_data.decode('utf-8')
		print(f"[Reçu] : {in_msg}")


server, port = ('192.168.1.23', 5566)

socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

socket.connect((server, port))
print('Connecté !')

thread_envoi = Thread(target=send_server, args=[socket])
thread_recv = Thread(target=recv_server, args=[socket])

thread_envoi.start()
thread_recv.start()