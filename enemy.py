import pygame as pg
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, pos, images):
        super().__init__(size, pos, images)
        
        self.direction = pg.math.Vector2(0,0)
        self.speed = -1
        self.gravity = 0.8
        
    def move(self):
        self.rect.x += self.speed
        
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def reverse(self):
        self.speed *= -1
        
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()