import socket
from _thread import *
from player import Player
import pickle

from random import randint

server, port = 'XXX.XXX.XXX.XXX', 5555
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

try:
    server_socket.bind((server, port))
except socket.error as e:
    print(e)

server_socket.listen()
print("[Server] : En attente de connexions...")

# liste des joueurs connectés
# 1: <Player>, 2:<Player>, ...
players = {}

client_number = 0

"""
Thread propre à chaque client
"""
def threaded_client(client, player_uid):
    global client_number
    # envoie l'obj <Player>, correspondant au player_uid, au client
    client.send(pickle.dumps(players[player_uid]))

    while True: # tant que le client est connecté
        try:
            # récupère le nouvel obj <Player> (envoyé par le client) -> type(data) = dict
            data = pickle.loads(client.recv(2048))
            players[player_uid] = data  # met a jour l'obj <Player> coté serveur /!\ pas de vérification /!\

            if not data:
                print("Déconnecté !")
                break

            else:
                print("[Reçu] :", data)

                print("[Envoi] :", players)

            client.sendall(pickle.dumps(players)) # envoie le dict de tout les joueurs au client propriétaire du thread

        # Si un joueur se déconnecte, alors client.recv() renvoie une erreur
        except EOFError as e:
            print(e)
            break

        except socket.error as e:
            print(e)
            break

    # si le client se déconnecte, on supprime l'obj <Player> correspondant
    print("Connexion perdue...")
    client.close()
    del players[player_uid]

"""
Création d'un thread différent pour chaque 
client tant que le serveur est en marche
"""
while True:
    connection, address = server_socket.accept()
    print("Connecté à :", address)

    print("[----- DEBUG -----] players :", players)
    color = (randint(100, 255), randint(100, 255), randint(100, 255))

    # créé une nouvelle instance de <Player>
    players[client_number] = Player(color, 0, 0, 40, 40, client_number)

    # démarrage d'un thread pour chaque nouvelle connexion (non bloquant)
    start_new_thread(threaded_client, (connection, client_number))

    client_number += 1