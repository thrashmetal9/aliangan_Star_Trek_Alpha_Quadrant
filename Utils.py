from Settings import*
import pygame as pg

class Map:
    def __init__(self, filename):
        # creates empty list for map data
        self.data = []
        # Allows us to open specific files and allows us to close the file automatically with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        # self.tilewidth makes properties of Map that define both length and width 
        #also allows for changing properties depending on settings inputted in this file
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * 32
        self.height = self.tileheight * 32

class Cooldown:
    def __init__(self, time):
        self.time = time
        self.start_time = pg.time.get_ticks()
    def start(self):
        self.start_time = 0
    def ready(self): 
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.time:
            return True
        return False

# loads image file and creates an image surface for bliting or drawing images on the surface
# class Spritesheet:
#     def __init__(self,filename):
#         self.spritesheet = pg.image.load(filename).convert()

#     def get_image(self, x ,y, width,height):
#         image = pg.Surface((width,height))
#         image.blit(self.spritesheet, (0,0), (x,y, width, height))
#         image = pg.transform.scale(image, (width // 2, height // 2))
#         return image 


