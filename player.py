import pygame as pg

class Player:
    def __init__(self, color, x, y, width, height, player_id):
        self.pos = [x, y]
        self.color = color
        self.rect = pg.Rect(x, y, width, height)
        self.speed = 3 # pixels / ticks

        self.uid = player_id

    def draw(self, s):
        pg.draw.rect(s, self.color, self.rect)

    def move(self):
        keys = pg.key.get_pressed()
        if keys[ord('z')]:
            self.pos[1] -= self.speed
        if keys[ord('q')]:
            self.pos[0] -= self.speed
        if keys[ord('s')]:
            self.pos[1] += self.speed
        if keys[ord('d')]:
            self.pos[0] += self.speed
        self.update()

    def update(self):
        self.rect.center = self.pos.copy()