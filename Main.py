#Aiden Aliangan
#Mr. Cozart
#Computer Programming / Period: 2
# October 25, 2025

#Design Goals:
#Design an interactive Player Sprite that can kill mobs

#Mechanical Goals: 
#Players can move ship on x and y axis 
#Players can only make ranged attacks
#Sound effects for Music, lasers being fired, and when ships get hit 
#Design a path system for Mob 
#Use an image for Sprites for Player and Mob 

#Rules:
#Players cannot collide with the end of the map or the game ends
#Players also cannot collide with an enemy mob or else health is lost 
#Players cannot fire upon their own base as the objective is to defend 


import math
import random
import sys 
import pygame as pg
from Settings import * 
from Sprites import *
from os import path
from Utils import *
from math import floor

class Game: 
    def __init__(self):
      pg.init()
      self.clock = pg.time.Clock()
      self.screen = pg.display.set_mode((WIDTH, HEIGHT))
      pg.display.set_caption("Aiden Aliangan's awesome game!!!!!")
      self.playing = True
      self.running = True 
      #set up a game folder directory path using the current folder containing THIS file 
#Gives the Geme class a map property which uses the Map class to parse the level2.txt file 
    def load_data(self):
      #Current directory for path
      #Create all sprite groups
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'images')
      self.map = Map(path.join(self.game_folder, 'level2.txt'))
      # loads image into memory when a new game is created. 
      # This goes into the images folder of the My_Game_Engine_Project 
      #This pulls the image to place for the sprite. Calls on folder where the image is located and imports it. 
      #Assings the sprite an image
      self.player_img = pg.image.load(path.join(self.img_folder, 'U.S.S._Enterprise_A.png')).convert_alpha()
      self.player_img = pg.transform.scale(self.player_img,(110,50))
      self.player_img_inv = pg.image.load(path.join(self.img_folder, 'U.S.S._Enterprise_A_flipped.png.png')).convert_alpha()
      self.player_img = pg.transform.scale(self.player_img, (110,50))
      self.player_img_up = pg.image.load(path.join(self.img_folder, 'U.S.S._Enterprise_A_UP.png')).convert_alpha()
      #pg.transform.scale allows rescaling specific imported images. In this case, for players, mobs, etc.
      self.player_img = pg.transform.scale(self.player_img,(110,50))
      self.player_img_down = pg.image.load(path.join(self.img_folder, 'U.S.S._Enterprise_A_DOWN.png')).convert_alpha()
      self.player_img = pg.transform.scale(self.player_img, (110,50))
      self.mob_img = pg.image.load(path.join(self.img_folder, 'klingon_BOP.png.png')).convert_alpha()
      self.mob_img_inv = pg.image.load(path.join(self.img_folder,'klingon_BOP_RIGHT.png')).convert_alpha()
      self.mob_img_down = pg.image.load(path.join(self.img_folder,'klingon_BOP_DOWN.png')).convert_alpha()
      self.mob_img_left = pg.image.load(path.join(self.img_folder,'klingon_BOP_LEFT.png')).convert_alpha()
      #loads image from the images folder and assigning it to become the background image for the game
      self.bg_img = pg.image.load(path.join(self.img_folder,'Space_Wallpaper.png')).convert_alpha()
      self.bg_img = pg.transform.scale(self.bg_img,(WIDTH, HEIGHT))

    def new(self):
      # the sprite Group allows us to upate and draw sprite in grouped batches using imported files, etc.
      # SPRITE is the visual elements on the screen of our code  
      #Adding things to our new game, mobs, Players, etc.
      self.load_data()
      self.all_sprites = pg.sprite.Group()
      self.all_mobs = pg.sprite.Group()
      self.all_coins = pg.sprite.Group()
      self.all_walls = pg.sprite.Group()
      self.all_projectiles = pg.sprite.Group()
       #instantiation of the player class in self.player which is a property of our game 
      self.player = Player(self, 100, 100)
      #For loop for adding mob
      for i in range(5):
         x = random.randint(10,WIDTH)
         y = random.randint(10,HEIGHT)
         m = Mob(self,x,y)
         self.all_sprites.add(m)
         self.all_mobs.add(m)
      for i in range(15):
         x = random.randint(10,WIDTH)
         y = random.randint(10,HEIGHT)
        #  c = Coin(self,x,y)
        #  self.all_sprites.add(c)
        #  self.all_coins.add(c)
      for row, tiles, in enumerate(self.map.data):
         print(row)
         for col,tile, in enumerate(tiles):
            print(col)
            if tile == '1':
               Wall(self, col, row, "")
            if tile == '2':
               Wall(self,col,row, "moveable")
            # elif tile == 'C':
            #    Coin(self,col,row)
            elif tile == 'P':
               self.player = Player(self,col,row)
            elif tile == 'M':
               Mob(self,col,row)

#Passing Mob class into the class of game so that it has access to the game

      self.all_sprites.add(self.player)
      # self.all_sprites.add(self.all_mobs)
     
    
      # self.all_sprites.add(self.mob)
    def run(self):
        while self.playing == True:
            self.dt = self.clock.tick(FPS)/1000
            # input
            self.events()
            # process
            self.update()
            # output
            self.draw()
        pg.quit()

    def events(self):
        #Game behavior when user interacts 
        for event in pg.event.get():
            if event.type == pg.QUIT:
            #  print("this is happening")
                self.playing = False
                if self.playing: 
                    self.playing = False
                self.running = False 
            if event.type == pg.MOUSEBUTTONDOWN:
                print("I can get input from mousey mouse mouse mousekerson")
    def update(self):
        self.all_sprites.update()
        seconds = (pg.time.get_ticks()//1000)
        countdown = 10
        self.time = countdown - seconds


    def draw_text(self, surface, text, size, color, x, y):
            font_name = pg.font.match_font('arial')
            font = pg.font.Font(font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (x,y)
            surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.screen.fill(WHITE)
        self.screen.blit(self.bg_img,(0,0))
        self.draw_text(self.screen, str(self.player.health), 24, WHITE,100,100)
        self.draw_text(self.screen, str(self.player.coins), 24, WHITE,400,100)
        self.draw_text(self.screen, str(pg.time.get_ticks()//1000),24, WHITE, 500,100)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def show_start_screen(self):
        # game splash/start screen
      #   pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
      #   pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text(self.screen,"Hello there!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
if __name__ == "__main__":
#    creating an instance or instantiating the Game class
    g = Game()
    g.new()
    g.run()
    g.show_start_screen()
    while g.running:
        g.new()
        g.run()

#Sources: Mr. Cozart's course resources code 
# ChatGPT
# Mr.Cozart's Github Link 