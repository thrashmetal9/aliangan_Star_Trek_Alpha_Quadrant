import pygame as pg
from pygame.sprite import Sprite
from Settings import * 
from Utils import Cooldown 
# from Utils import Spritesheet
from random import randint
from random import choice
from os import path
vec = pg.math.Vector2

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


#Initiating Player Class / Super Class as it is able to create surface, get rectangle 
#Sprite is a visual element on the spring
#Defining Properties for the Player Sprite 
class Player(Sprite):
    def __init__(self, game, x, y):
        Sprite.__init__(self)
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        self.image = pg.Surface((32, 32))

        # self.image.fill(GREEN)
        self.image = game.player_img
        # self.spritesheet = Spritesheet(path.join(self.game.img_folder("spritesheet.png")))
        # self.load_images()
        #Set_Color key gets rid of the background for the imported image
        self.image.set_colorkey(BLACK)
        #game.player_img_inv sets the image for the sprite 
        #Load of images imported into the Sprites file from Main
        #Use for Transform Flip / Extra detail for when players control the ship, the image can be rotated
        self.image_inv = game.player_img_inv
        self.image_up = game.player_img_up
        self.image_down = game.player_img_down
        self.rect = self.image.get_rect()
        #gives the player sprite motion
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.speed = 250
        self.health = 100
        self.coins = 0
        self.bullets = 10
        self.cd = Cooldown(1000)
        self. dir = vec(0,0)
        self.flying = False
        self.last_update = 0
        self.jump_power = 100
        self.facing = ""
    # def jump(self):
    #     hits = pg.sprite.collide(self, self.game.all_walls, False)
    #     self.rect.y += 1
    #     hits = pg.sprite.spritecollide(self,self.game.all_walls)
    #     if hits: 
    #         self.vel.y = -self.jump_power  
    # def load_images(self):
    #     self.standing_frames = [self.spritesheet.get_image(0,0,32,32),
    #                             self.spritesheet.get_image(0,32,32,32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(WHITE)
            # self.walk_frames_r
            # self.walk_frames_l
            # pg.transform.flip

    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.flying: 
    #         if now - self.last_update > 350:
    #             print(now)
    #         self.last_update = now
    #         self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #         bottom = self.rect.bottom 
    #         self.image = self.standing_frames[self.current_frame]
    #         self. rect = self.image.get_rect()
    #         self.rect.bottom = bottom 

#Using if statements to determine specific actions when specific keys are pressed. Specifically, the code aims to 
#target WASD keys 
#Allow players to move ship along the x or y axis 
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]: 
            self.jump()
        # if keys[pg.K_e]:
            # p = Projectile(self.game, self.rect.x, self.rect.y, self.dir)
        #Used Chat GPT to help with the transform flip vertically. 
        if keys[pg.K_w]:
            self.vel.y = -self.speed*self.game.dt
            self.dir = vec(0,-1)
            if self.facing != "up":
                self.facing = "up"
                self.flipped_img = pg.transform.rotate(self.image, 90)
                self.image = self.flipped_img
            # self.rect.y -= self.speed
            #pg.transform.rotate rotates the image of the player. 
            #Ensures if a certain key of WASD is pressed, the image rotates to face a certain direction
        if keys[pg.K_a]:
            self.vel.x = -self.speed*self.game.dt
            self.dir = vec(-1,0)
            if self.facing != "left":
                self.facing = "left"
                self.flipped_img = pg.transform.flip(self.image, True, False)
                self.image = self.flipped_img
            if self.facing == "left":
                self.dir = vec(-1,0)
            # self.rect.x -= self.speed
            #Used Chat GPT to help with flipping image principles vertically. 
        if keys[pg.K_s]:
            # self.vel.y = self.speed*self.game.dt
            self.vel.y = self.speed*self.game.dt
            self.dir = vec(0,1)
            if self.facing != "down":
                self.facing = "down"
                self.image_down = pg.transform.rotate(self.image, 270)
                #pg.transform.rotate rotates the image and 270 is the parameter for the number of degrees to rotate the image
                self.image = self.image_down
                #self.image= self.image_down is the new condition or the new variable to self.image once condition is met
            # self.rect.y += self.speed
        if keys[pg.K_d]:
            self.vel.x = self.speed*self.game.dt
            self.dir = vec(1,0)
            if self.facing != "right":
                self.facing = "right"
                self.flipped_img = pg.transform.flip(self.image, True, False)
                self.image = self.flipped_img 
            if self.facing == "right":
                self.dir = vec(1,0)
        
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    if hits[0].state == "moveable":
                        print("I hit a moveable black")
                        hits[0].pos.x += self.vel.x 
                        if hits [1].rect.left - self.rect.width:
                            print("second element")
                    #Using collide with walls method to check which wall is moveable and also use it to move specific blocks
                    # hits [0] is the first wall hit or whatever we had just hit
                else:
                    self.pos.x = hits[0].rect.left - self.rect.width
                    #position would be subracted by the width after colliding with wall
                if self.vel.x < 0:
                    if hits[0].state == "moveable":
                        print("I hit a moveable black")
                        hits[0].pos.x += self.vel.x 
                    else:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                # hits[0].vel.x = 0
                self.rect.x = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    hits[0].pos.y += self.vel.y  
                    self.pos.y = hits[0].rect.top - self.rect.height
                else:
                    self.pos.y = hits[0].rect.bottom - self.rect.height
                if self.rect.y < 0:
                    hits[0].pos.y += self.vel.y
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                
    
    def collide_with_stuff(self, group, kill):
    #self is always important with every module as in this case, it relates to calling on collisions with the player
        hits = pg.sprite.spritecollide(self, group, kill)
        #Constantly checking and returning values to determine whether player has made contact with group or killed it
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                if self.cd.ready():
                    self.health -= 10
                print(self.health)
            if str(hits[0].__class__.__name__) == "Coin":
                print("i collided with a coin")
                self.coins += 1
                print(self.coins)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    # hits [0] is the first wall hit or whatever we had just hit
                    self.pos.x = hits[0].rect.left - self.rect.width
                    #position would be subracted by the width after colliding with wall
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
            if hits: 
                if self.vel.y > 0:
                    self.pos.y = hits[1].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[1].rect.bottom          
            self.vel.y = 0
                # # hits[0].vel.x = 0
            self.rect.y = self.pos.y
    #Defining behaior for the Player sprite 
    def update(self):
        # self.effects_trail()
        self.get_keys()
        # self.animate()
        self.pos += self.vel 
        # dt is a delta time
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y') 
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_coins, True)
        if not self.cd.ready():
            self.image_inv = self.game.player_img_inv
            print("not ready")
        else:
            self.image = self.game.player_img
            print("ready")
# Player behavior regarding flipping the image for the sprite
# This is my own work this time  
        if self.facing == "left":
            self.flipped_img = pg.transform.flip(self.image, True, False)
            self.image = self.flipped_img
        if self.facing == "up":
            self.flipped_img = pg.transform.rotate(self.image, 90)
            self.image = self.flipped_img
        if self.facing == "down":
            self.flipped_img = pg.transform.rotate(self.image, 270)
            self.image = self.flipped_img
    # def effects_trail(self):
    #     if self.effect_cd.ready():
    #         EffectTrail(self.game, self.rect.x,self.rect.y)
        # print(self.cd.ready())    
        # if not self.cd.ready():
        #     self.image.fill(BLUE)
        #     print("Not Ready")
        # else:
        #     self.image.fill(GREEN)
        #     print("Ready")
#Initiating Class Mob by defining speciic properties, characteristics, and adding them to my game 
class Mob(Sprite): 
    #Defining specific properties and certain dimmensions and characteristics for Mob
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        # self.spritesheet = Spritesheet(path.join(self.game.img_folder, "spritesheet.png"))
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        #Loads the image assigned to the mob - defining the physical attributes or properties of the mob
        self.image = game.mob_img
        self.fade = 255
        # self.image.fill(RED)
        #Gets rid of background image and also any part of the mob that is black
        self.image.set_colorkey(BLACK)
        self.image_inv = game.mob_img_inv
        self.image_down = game.mob_img_down
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        #Gives the mob movement 
        # self.vel = vec(choice([1,1]), choice([-1,1]))
        self.vel = vec(0,0)
        self.pos = vec(x,y)*TILESIZE[0]
        self.health = 100 
        self.speed = 5
        self.cd = Cooldown(1000)
        self.facing = "up"
    # def collide_with_walls(self, dir):
    #     self.vel.y *= choice([-1,1])
        # if dir == 'x':
        #     hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
        #     if hits:
        #         if self.vel.x > 0:
        #             # hits [0] is the first wall hit or whatever we had just hit
        #             self.pos.x = hits[0].rect.left - self.rect.width
        #             #position would be subracted by the width after colliding with wall
        #         if self.vel.x < 0:
        #             self.pos.x = hits[0].rect.right
        #         # self.vel.x = 0
        #         self.rect.x = self.pos.x
        #         self.vel.x *= choice([-1,1])
                #choice randomly picks the integer from the two given values 
                #Lists and it will pick something from the list
        # if dir == 'y':
        #     hits = pg.sprite.spritecollide(self,self.game.all_walls, False)
        #     if hits:
        #         if self.vel.y > 0:
        #             self.pos.y = hits[0].rect.top - self.rect.height
        #         if self.rect.y < 0:
        #             self.pos.y = hits[0].rect.bottom 
        #         self.rect.y = self.pos.y
        #         self.vel.y *= choice([-1,1])
   
    def movement(self):
        self.image = self.image
        if self.pos.x > 845:
            self.vel = vec(0, 1)
            if self.pos.y > 600:
                self.vel = vec(-1,0)
        if self.pos.x < 100 :
            self.vel = vec(0, -1)
            if self.pos.y < 100:
                self.vel = vec(1,0)
    #Above is a define in which gives the mob velocity and trajectory.
    #Trajectory is that the Mob takes a lap along the screen's primeter

    def check_dir(self):
        if self.vel.y > 0:
            if self.facing != "down":
                self.facing = "down"
                self.image_down = pg.transform.rotate(self.image,-90)
                self.image = self.image_down
            #rotates image clockwise to face a certain direction
            #Position is essential as it determines when the image must rotate
            #Most importantly, ensures the mob is facing the right direction when a certain condition is met
        if self.vel.x > 0:
            if self.facing != "right":
                self.facing = "right"
                self.image_right = pg.transform.rotate(self.image,-90)
                self.image = self.image_right
        elif self.vel.x < 0:
            if self.facing != "left":
                self.facing = "left"
                self.image_left = pg.transform.rotate(self.image, -90)
                self.image = self.image_left
        elif self.vel.y < 0: 
            if self.facing != "up":
                self.facing = "up"
                self.image_up = pg.transform.rotate(self.image, -90)
                self.image = self.image_up
                
    # def movement(self):
    #     if self.pos.x > 845:
    #         self.vel = vec(0, 1)
    #         if self.facing != "down":
    #             self.facing = "down"
    #             if self.pos.x > 100: 
    #                 self.image_down = pg.transform.rotate(self.image, 90)
    #                 self.image = self.image_down
    #         if self.pos.y < 600 :
    #             self.vel = vec(-1,0)
    #             if self.facing != "left":
    #                 self.facing = "left"
    #                 self.flipped_img = pg.transform.rotate(self.image, 90)
    #                 self.image = self.flipped_img
    #     if self.pos.x < 100 :
    #         self.vel = vec(0, -1)
    #         if self.facing != "up":
    #             self.facing = "up"
    #             self.image = self.image      
    #     if self.pos.y < 100 and self.pos.x < 100:
    #         self.vel = vec(1,0)
    #         if self.facing != "right": 
    #             self.facing = "right"
    #             self.flipped_img = pg.transform.rotate(self.image,90)
    #             self.image = self.flipped_img 
                
        
    def update(self):
        self.check_dir()
        self.movement()
        # if self.health <= 0:
        #     self.kill()
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        

        # self.collide_with_walls(self.game.all_weapons, False)
        # if self.pos.x > 845 :
        #     if self.image == self.image: 
        #         self.facing == "down"
        #         self.image_down = pg.transform.rotate(self.image, 180)
        #         self.image = self.image_down 
        #         self.image != self.image
        # if self.pos.y > 600:
        #     self.facing == "left"
        #     self.image_left = pg.transform.rotate(self.image, 270)
        #     self.image = self.image_left
        # if self.pos.x < 845 and self.pos.y < 100:
        #     if self.pos.y < 100:
        #         self.facing == "right"
        #         self.image_right = pg.transform.rotate(self.image, 90)
        #         self.image = self.image_right
           
        
       
        # if self.pos.x > 845:
        #     if self.facing == "down":
        #         if self.pos.x != 100:
        #             self.flipped_img = pg.transform.rotate(self.image, 90)
        #             self.image = self.flipped_img
        #         self.vel = vec(0,1)
        #     if self.pos.y < 600:
        #         if self.facing == "left":
        #             self.flipped_img = pg.transform.rotate(self.image,90)
        #             self.vel = vec(-1,0)
                   
        # if self.pos.x < 100 :
        #     if self.facing == "up":
        #         self.image = self.image 
        #     if self.pos.y < 100:
        #         if self.facing == "right":
        #             self.flipped_img = pg.transform.rotate(self.image, 90)
        #             self.image = self.flipped_img

        
     
        
        

      
    
        
class Wall(Sprite):
    def __init__(self,game, x, y, state):
        self.game = game
        self.groups = game.all_sprites,game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE[0]
        self.state = state
        # print("Wall created at", str(self.rect.x), str(self.rect.y))
    def update(self):
     #behavior of the wall 
     # 
     self.pos += self.vel
     self.rect.x = self.pos.x
     self.rect.y = self.pos.y

# class EffectTrail(Sprite):
#     def __init__(self, game, x, y):
#         self.game = game
#         self.groups = game.all_sprites
#         Sprite.__init__(self, self.groups)
#         self.image = pg.Surface(TILESIZE, pg.SRCALPHA)
#         self.alpha = 255
#         self.image.fill((255,255,255,255))
#         self.rect = self.image.get_rect()
#         self.cd = Cooldown(10)
#         self.rect.x = x
#         self.rect.y = y
#         # coin behavior
#         self.scale_x = 32
#         self.scale_y = 32
#     def update(self):
#         if self.alpha <= 10:
#             self.kill()
#         self.image.fill((255,255,255,self.alpha))
        
#         if self.cd.ready():
#             self.scale_x -=1
#             self.scale_y -=1
#             print("I'm ready")
#             self.alpha -= 50
#             new_image = pg.transform.scale(self.image, (self.scale_x, self.scale_y))
#             self.image = new_image 
    


# class RotatingSprite(pg.sprite.Sprite):
#     def __init__(self,game,image,pivot_pos, radius, angle_offset=0, rotate_with_orbit=False):
#         super().__init__()
#         self.game = game 
#         self.groups = game.all_sprites
#         self.image = game.player_img
#         self.original_image = self.image.convert_alpha()
#         self.image = self.original_image


#         self.pivot = pg.Vector2(pivot_pos) 
#         self.radius = radius 
#         self.angle = angle_offset
#         self.rotate_with_orbit = rotate_with_orbit 

#         self.rect = self.image.get_rect()
class Projectile(Sprite): 
    def __init__(self, game, x, y, dir):
        keys = pg.key.get_pressed()
        self.game = game
        self.groups = game.all_sprites, game.all_projectiles 
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((85, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = dir
        self.pos = vec(x,y)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        # if keys[pg.K_i]:
        #     self.image = pg.Surface((32,85))
        #     self.vel = vec(0,-1)
        #     self.pos = vec(x,y)
        #     self.speed = 10
    def update(self):
        self.pos += self.vel * self.speed
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            self.kill()
        #Hits all mobs
        if pg.sprite.spritecollideany(self, self.game.all_walls):
            self.kill()
            return
            