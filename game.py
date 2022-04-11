import pygame as pg
import sys
from settings import *
from level import Level
from sound import Sound

pg.init()
screen = pg.display.set_mode((screen_width,screen_height))
clock = pg.time.Clock()
sound = Sound()
level = Level(level_one, screen, sound)
bg = pg.image.load(f'images/level_bg.png')

sound.play_bg()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
    #screen.fill('black')
    #screen.blit(bg, (0,0))
    level.run()
    
    pg.display.update()
    clock.tick(60)    