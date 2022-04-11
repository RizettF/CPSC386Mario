from os import walk
import pygame as pg
from settings import tile_size

#Originally how I was going to import sprites
def import_folder(path):
    surface_list = []
    
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surface = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
            
    return surface_list

#Imports sprite sheet for tiles
def import_cut_graphic(path):
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    
    cut_tiles = []
    
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            
            new_surface = pg.Surface((tile_size, tile_size))
            new_surface.blit(surface, (0,0), pg.Rect(x,y,tile_size, tile_size))
            cut_tiles.append(new_surface)
            
    return cut_tiles