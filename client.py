from network import Network
import pygame as pg

class Client:
    def __init__(self):
        pg.init()
        self.width = 500
        self.height = 500
        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size)

        self.network = Network()
        # Le joueur que controle le client
        self.player = self.network.get_player()
        # Les autres joueurs
        self.other_players = self.network.send(self.player)

        self.clock = pg.time.Clock()

        self.running = True

        pg.display.set_caption(f"Client n°{self.player.uid}")

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

    def clear_screen(self):
        self.screen.fill((12, 12, 12))

    def draw_players(self, player_dict):
        for player in player_dict.values():
            player.draw(self.screen)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)

            # à chaque tick, on update les stats des autres joueurs
            self.other_players = self.network.send(self.player)
            print(self.other_players)

            self.events()

            self.clear_screen()
            self.player.move()
            self.draw_players(self.other_players)
            pg.display.update()

        print(f"Client déconnecté")
        pg.quit()

client = Client()
client.run()