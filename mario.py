import pygame as pg
from pygame.sprite import Sprite
from support import import_folder
import os.path

#This is the class that handles Mario and his movement
class Mario(Sprite):
    
    def __init__(self, pos, sound):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.3
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.sound = sound
        
        #movement
        self.direction = pg.math.Vector2(0,0)
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = -15
        
        #mario status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
    
    def import_character_assets(self):
        self.animations = {'idle':[], 'run':[], 'climb':[], 'jump':[], 'dead':[], 'skid':[]}
        
        self.animations['idle'] = [pg.image.load(f'images/idle/idle{n}.png') for n in range(1)]
        self.animations['run'] = [pg.image.load(f'images/run/run{n}.png') for n in range(3)]
        self.animations['climb'] = [pg.image.load(f'images/climb/climb{n}.png') for n in range(2)]
        self.animations['jump'] = [pg.image.load(f'images/jump/jump{n}.png') for n in range(1)]
        self.animations['dead'] = [pg.image.load(f'images/dead/dead{n}.png') for n in range(1)]
        self.animations['skid'] = [pg.image.load(f'images/skid/skid{n}.png') for n in range(1)]
    
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        
        #repeating the frame index
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        image = animation[int(self.frame_index)]    
        
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pg.transform.flip(image, True, False)
            self.image = flipped_image
    
    def get_input(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pg.K_SPACE]and self.on_ground:
            self.jump()
    
    def get_status(self):
        if self.on_ground is False:
            self.status = 'jump'
        elif self.direction.x == 0:
            self.status = 'idle'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'      
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
        self.sound.play_jump()
            
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()