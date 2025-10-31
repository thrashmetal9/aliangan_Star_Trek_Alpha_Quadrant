#Aiden Aliangan
#Mr. Cozart
#Computer Programming / Period: 2
# October 25, 2025

#yay I can use github from VS CODE!


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
      #set up a game folder directory path using the current folder containing THIS file 
#Gives the Geme class a map property which uses the Map class to parse the level1.txt file 
    def load_data(self):
      #Current directory for path
      #Create all sprite groups
      self.game_folder = path.dirname(__file__)
      self.img_folder = path.join(self.game_folder, 'images')
      self.map = Map(path.join(self.game_folder, 'level2.txt'))
      # loads image into memory when a new game is created. This goes into the images folder of the My_Game_Engine_Project 
      #This pulls the image to place for the sprite. Calls on folder where the image is located and imports it. 
      self.player_img = pg.image.load(path.join(self.img_folder, 'U.S.S._Enterprise_A.png')).convert_alpha()
      self.player_img_inv = pg.image.load(path.join(self.img_folder, 'U.S.S._Enterprise_A.png')).convert_alpha()

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
            #  print("this is happening")
                self.playing = False
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
        self.draw_text(self.screen, str(self.player.health), 24, BLACK,100,100)
        self.draw_text(self.screen, str(self.player.coins), 24, BLACK,400,100)
        self.draw_text(self.screen, str(pg.time.get_ticks()//1000),24, BLACK, 500,100)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

if __name__ == "__main__":
#    creating an instance or instantiating the Game class
    g = Game()
    g.new()
    g.run()
