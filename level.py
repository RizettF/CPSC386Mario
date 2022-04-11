import pygame as pg
from support import import_cut_graphic
from tiles import AnimatedTile, Qblock, Tile
from settings import tile_size, screen_width
from mario import Mario
from sound import Sound
from enemy import Enemy

class Level():
    
    #Setting up level
    def __init__(self, data, surface, sound):
        self. tile_set = self.import_tile_assets()
        self.display_surface = surface
        self.level_setup(data, sound)
        self.world_shift = 0
        
    #Importing tile sprites
    def import_tile_assets(self):
        
        tile_set = import_cut_graphic('images/tiles/tiles2.png')
        #self.hill = import_cut_graphic('images/tiles/hill.png')
        self.hill = [pg.image.load(f'images/tiles/hill{n}.png') for n in range(6)]
        self.ground = tile_set[0]
        self.brick = tile_set[1]
        self.block = tile_set[29]
        self.q_block = [tile_set[23], tile_set[24], tile_set[25]]
        self.pipes = [tile_set[232], tile_set[233], tile_set[261], tile_set[262]]
        self.i_block = pg.image.load(f'images/tiles/clear.png').convert_alpha()
        self.pole = [tile_set[277], tile_set[248]]
        self.flag = pg.image.load(f'images/tiles/goal_flag.png').convert_alpha()
        self.sky_tile = pg.image.load(f'images/tiles/sky.png').convert_alpha()
        self.bush = [tile_set[272], tile_set[273], tile_set[274]]
        
        self.goomba = []
        self.goomba.append(pg.image.load(f'images/goomba.png').convert_alpha())
        self.goomba.append(pg.transform.flip(self.goomba[0], True, False))
        
        
        
        return tile_set
    
    #Setting up the level and its various tiles            
    def level_setup(self, layout, sound):
        self.sky_bg = pg.sprite.Group()
        self.bg = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.mario = pg.sprite.GroupSingle()
        
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                
                sky = Tile((x,y), tile_size, self.sky_tile)
                self.sky_bg.add(sky)
                
                if cell == 'X':
                    tile = Tile((x,y), tile_size, self.ground)
                    self.tiles.add(tile)
                elif cell == 'B':
                    tile = Tile((x,y), tile_size, self.brick)
                    self.tiles.add(tile)
                elif cell == 'S':
                    tile = Tile((x,y), tile_size, self.block)
                    self.tiles.add(tile)
                elif cell == 'Q':
                    tile = Qblock((x, y), tile_size, self.q_block)
                    self.tiles.add(tile)
                elif cell == 'L':
                    tile = Tile((x,y), tile_size, self.pipes[0])
                    self.tiles.add(tile)
                elif cell == 'R':
                    tile = Tile((x,y), tile_size, self.pipes[1])
                    self.tiles.add(tile)
                elif cell == 'l':
                    tile = Tile((x,y), tile_size, self.pipes[2])
                    self.tiles.add(tile)
                elif cell == 'r':
                    tile = Tile((x,y), tile_size, self.pipes[3])
                    self.tiles.add(tile)
                elif cell == 'I':
                    tile = Tile((x,y), tile_size, self.i_block)
                    self.tiles.add(tile)
                elif cell == 'G':
                    enemy = Enemy((x,y), tile_size, self.goomba)
                    self.enemies.add(enemy)
                elif cell == 'P':
                    tile = Tile((x,y), tile_size, self.pole[0])
                    self.tiles.add(tile)
                elif cell == 'T':
                    tile = Tile((x,y), tile_size, self.pole[1])
                    self.tiles.add(tile)
                elif cell == 'F':
                    tile = Tile((x,y), tile_size, self.flag)
                    self.tiles.add(tile)
                elif cell == '0':
                    bg = Tile((x,y), tile_size, self.hill[0])
                    self.bg.add(bg)
                elif cell == '1':
                    bg = Tile((x,y), tile_size, self.hill[1])
                    self.bg.add(bg)
                elif cell == '2':
                    bg = Tile((x,y), tile_size, self.hill[2])
                    self.bg.add(bg)
                elif cell == '3':
                    bg = Tile((x,y), tile_size, self.hill[3])
                    self.bg.add(bg)
                elif cell == '4':
                    bg = Tile((x,y), tile_size, self.hill[4])
                    self.bg.add(bg)
                elif cell == '5':
                    bg = Tile((x,y), tile_size, self.hill[5])
                    self.bg.add(bg)    
                elif cell == 'M':
                    mario_sprite = Mario((x,y), sound)
                    self.mario.add(mario_sprite)
    
    #Acts as the games camera
    def scroll_x(self):
        mario = self.mario.sprite
        mario_x = mario.rect.centerx
        direction_x = mario.direction.x
        
        if mario_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            mario.speed = 0
        elif mario_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            mario.speed = 0
        else:
            self.world_shift = 0
            mario.speed = 8
     
    #Checks if mario is running into a wall
    def horizontal_movement_collision(self):
        mario = self.mario.sprite
        mario.rect.x += mario.direction.x * mario.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(mario.rect):
                if mario.direction.x < 0:
                    mario.rect.left = sprite.rect.right
                elif mario.direction.x > 0:
                    mario.rect.right = sprite.rect.left
    
    #Checks if mario is standing or hitting a brick                
    def vertical_movement_collision(self):
        mario = self.mario.sprite
        mario.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(mario.rect):
                if mario.direction.y > 0:
                    mario.rect.bottom = sprite.rect.top
                    mario.direction.y = 0
                    mario.on_ground = True
                    
                elif mario.direction.y < 0:
                    mario.rect.top = sprite.rect.bottom
                    mario.direction.y = 0
          
        if mario.on_ground and mario.direction.y < 0 or mario.direction.y > 1:
            mario.on_ground = False
    
    #Checks if enemy runs into wall        
    def enemy_collision_reverse(self):
        for enemy in self.enemies.sprites():
            if pg.sprite.spritecollide(enemy, self.tiles, False):
                enemy.reverse()
    
    #Checks if enemy is falling
    #This causes some enemies to glitch out when colliding with edges          
    def enemy_vertical_movement(self):
        for enemy in self.enemies:
            enemy.apply_gravity()
            
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
            
        
               
    def run(self):
        self.sky_bg.update(self.world_shift)
        self.sky_bg.draw(self.display_surface)
        
        self.bg.update(self.world_shift)
        self.bg.draw(self.display_surface)
        
        #Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        #enemies
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display_surface)
        self.enemy_collision_reverse()
        self.enemy_vertical_movement()
        
        #Mario
        self.mario.update()
        self.mario.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()