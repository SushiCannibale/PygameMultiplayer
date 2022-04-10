import socket
import pickle

"""
Le network fait le lien entre le serveur et le client
"""
class Network:
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server = 'XXX.XXX.XXX.XXX' # ip du server
        self.port = 5555
        self.address = (self.server, self.port)

        # récupère le joueur initialement envoyé par le serveur
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            pickle_data = pickle.loads(self.client.recv(2048))
            return pickle_data
        except socket.error as e:
            print(e)

    # envoie des données au serveur
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data)) # envoie des données au client
            return pickle.loads(self.client.recv(2048)) # récupère la réponse du serveur et l'envoie au client
        except socket.error as e:
            print(e)