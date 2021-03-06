import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from maploader import *
from Debug import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(10, 50)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder,'Maps\\Map0.txt'))
        
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bgs = pg.sprite.Group()
        #create map
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '.' or 'p':
                    Bg(self,col,row)
                if tile == '1':
                    Wall(self,col,row)
                if tile == 'p':
                    self.player = Player(self,col,row)
        self.camera = Camera(self.map.width,self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        if SHOWFPS:
            print(self.clock)
            pg.display.set_caption(str(self.clock))
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.TrackSprite(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            if sprite.zlevel == 0:
                self.screen.blit(sprite.image,self.camera.apply(sprite)) 
        for sprite in self.all_sprites:
            if sprite.zlevel != 0:
                self.screen.blit(sprite.image,(self.camera.apply(sprite)[0] - (15 * (PLAYER_SIZE / 64)),self.camera.apply(sprite)[1] - (17*(PLAYER_SIZE / 64))))
        if DRAWPLAYERHITBOX == True: 
            pg.draw.rect(self.screen,WHITE,self.camera.apply(self.player),2)
        #self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def music(self):
        pass

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()