from network import Network
import pygame as pg
from threading import Thread

class Client:
    def __init__(self):
        pg.init()
        self.width = 500
        self.height = 500
        self.size = (self.width, self.height)
        self.screen = pg.display.set_mode(self.size)

        self.network = Network()
        self.player = self.network.get_player() # Peut valoir <None>
        self.other_players = self.network.send(self.player)  # Les autres joueurs

        self.clock = pg.time.Clock()

        self.running = True

        self.no_server_thread = Thread(target=self.wait_for_server)

        self.font = pg.font.SysFont("Arial", 20)

        self.rect_id = 0
        self.rect_height = 20
        self.triple_rect = [pg.Rect(self.width // 2 - 100, self.height // 2 + 50, 10, 10),
                            pg.Rect(self.width // 2 - 50, self.height // 2 + 50, 10, 10),
                            pg.Rect(self.width // 2, self.height // 2 + 50, 10, 10),
                            pg.Rect(self.width // 2 + 50, self.height // 2 + 50, 10, 10),
                            pg.Rect(self.width // 2 + 100, self.height // 2 + 50, 10, 10)]

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

    def wait_for_server(self):
        while not self.player and self.running:
            self.player = self.network.connect_player()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.events()
            self.clear_screen()

            if self.player:
                pg.display.set_caption(f"Client n°{self.player.uid} - {self.clock.get_fps():.2f} FPS")

                # à chaque tick, on update les stats des autres joueurs
                self.other_players = self.network.send(self.player)

                print("acc :", self.player.acc, "vel :", self.player.vel)


                self.player.move()
                self.draw_players(self.other_players)

            elif not self.no_server_thread.is_alive():
                self.no_server_thread.start()

            else:
                self.draw_smooth_text("En attente du server...", (self.width // 2, self.height // 2))
                pg.draw.rect(self.screen, (255, 255, 255), self.triple_rect[self.rect_id])
                pg.time.wait(100)
                self.rect_id = (self.rect_id + 1) % len(self.triple_rect)

            pg.display.update()

        print("Client déconnecté")
        pg.quit()

    def draw_smooth_text(self, text, center_pos):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = center_pos
        self.screen.blit(text_surface, text_rect)

client = Client()
client.run()
pg.quit()