import pygame as pg
from pygame.sprite import Sprite

class Tile(Sprite):
    def __init__(self, pos, size, tile):
        super().__init__()
        self.image = tile
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift
        
class AnimatedTile(Tile):
    def __init__(self, pos, size, tiles):
        super().__init__(pos, size, tiles[0])
        self.frames = tiles
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self):
        self.frame_index += 0.15
        
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        self.image = self.frames[int(self.frame_index)]
        
    def update(self, shift):
        self.animate()
        self.rect.x += shift
        
class Qblock(AnimatedTile):
    def __init__(self, pos, size, tiles):
        super().__init__(pos, size, tiles)