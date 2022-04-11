import pygame as pg
Vec = pg.Vector2

class Player:
    def __init__(self, color, x, y, width, height, player_id):
        self.pos = [x, y]
        self.size = (width, height)
        self.color = color
        self.rect = pg.Rect(x, y, width, height)

        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

        self.uid = player_id

        # liste des projectiles tirés par le joueur (actuellement à l'écran)
        self.projectiles = []

    def draw(self, s):
        pg.draw.rect(s, self.color, self.rect)

    def move(self):
        self.acc = Vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[ord('z')]:
            self.acc.y = -1
        if keys[ord('q')]:
            self.acc.x = -1
        if keys[ord('s')]:
            self.acc.y = +1
        if keys[ord('d')]:
            self.acc.x = +1
        self.update()

    def update(self):
        self.acc += self.vel * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.wrap_velocity()

        self.wrap_player()

        self.rect.center = self.pos

    def wrap_velocity(self):
        if round(self.vel.x, 2) == 0:
            self.vel.x = 0
        if round(self.vel.y, 2) == 0:
            self.vel.y = 0

    def wrap_player(self):
        if self.pos[0] < self.size[0] // 2:
            self.pos[0] = 0 + self.size[0] // 2
        if self.pos[1] < self.size[1] // 2:
            self.pos[1] = 0 + self.size[1] // 2
        if self.pos[0] > (500 - self.size[0] // 2):
            self.pos[0] = 500 - self.size[0] // 2
        if self.pos[1] > (500 - self.size[1] // 2):
            self.pos[1] = 500 - self.size[1] // 2