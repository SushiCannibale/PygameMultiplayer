import socket
from threading import Thread

def send_client(client):
	while True:
		msg = str(input("> "))
		data = msg.encode('utf-8')
		client.sendall(data)
		print(f"Envoyé : {msg}")

def recv_client(client):
	while True:
		in_data = client.recv(1024)
		in_msg = in_data.decode('utf-8')
		print(f"[Reçu] : {in_msg}")
		if not in_msg:
			print("Connexion perdue :'(")
			break

server, port = ('192.168.1.23', 5566)

socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket.bind((server, port))

socket.listen()
client, address = socket.accept()

thread_envoi = Thread(target=send_client, args=[client])
thread_recv = Thread(target=recv_client, args=[client])

# démarre l'async
thread_envoi.start()
thread_recv.start()

# attends la fin des threads pour close
thread_recv.join()

client.close()
socket.close()
