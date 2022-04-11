import pygame as pg

#This is the sound class that controls sound for the game
class Sound:
    def __init__(self):
        pg.mixer.init()
        self.end_theme = pg.mixer.Sound('sounds/SMB_gameover.wav')
        self.death = pg.mixer.Sound('sounds/SMB_mariodie.wav')
        self.jump = pg.mixer.Sound('sounds/SMB_high_jump.wav')
        
    def play_music(self, music, volume = 0.3):
        pg.mixer.music.unload()
        pg.mixer.music.load(music)
        pg.mixer.music.set_volume(volume)
        pg.mixer.music.play(-1, 0.0)
    
    def busy(self):
        return pg.mixer.get_busy()
    
    def play_sound(self, sound):
        pg.mixer.Sound.play(sound)
    
    def play_jump(self):
        self.play_sound(self.jump)
    
    def play_bg(self):
        self.play_music('sounds/SMB_Theme.wav')
        
    def play_game_over(self):
        self.stop_bg()
        self.play_sound(self.end_theme)
        while self.busy():
            pass
        
    def stop_bg(self):
        pg.mixer.music.stop()