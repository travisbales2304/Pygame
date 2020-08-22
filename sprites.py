import pygame as pg
from settings import *
import math



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.playerlastDirection = 0
        self.framecounter = 0
        self.framenumber = 0
        self.PlayerFramePosition = 0
        self.zlevel = 1
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        '''
        Player Velocity
        '''
        self.vx = 0
        self.vy = 0

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        
        self.spritesheetIdle = pg.image.load('GameAssets\\Roon.png').convert_alpha()
        self.spritesheetRun = pg.image.load('GameAssets\\Kings and Pigs\\Sprites\\01-King Human\\Run (78x58).png').convert_alpha()
        self.spritesheet = self.spritesheetIdle
        self.image = self.get_image(0,0,32,32)
        self.image = pg.transform.scale(self.image,(PLAYER_SIZE,PLAYER_SIZE))
        self.image.set_colorkey(BLACK)
        #self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        

    def get_keys(self):
        self.framecounter += 1
        self.vx,self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED
            self.playerlastDirection = 1
            if self.framecounter % 7 == 0:
                self.spritesheet = self.spritesheetRun
                self.image = self.get_image((self.framecounter % 8 * 78),0,78,58)
                self.image = pg.transform.scale(self.image,(PLAYER_SIZE,PLAYER_SIZE))
                self.image.set_colorkey(BLACK)
                self.image = pg.transform.flip(self.image, True, False)
        elif keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED
            self.playerlastDirection = 0
            if self.framecounter % 7 == 0:
                self.spritesheet = self.spritesheetRun
                self.image = self.get_image((self.framecounter % 8 * 78),0,78,58)
                self.image = pg.transform.scale(self.image,(PLAYER_SIZE,PLAYER_SIZE))
                self.image.set_colorkey(BLACK)
        elif keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED
        elif keys[pg.K_DOWN]:
            self.vy = PLAYER_SPEED
        else:
            if self.framecounter % PLAYER_ANIM_SPEED == 0:
                self.framenumber += 1
                if self.framenumber > 6:
                    self.framenumber = 1
                self.spritesheet = self.spritesheetIdle
                self.image = self.get_image((self.framenumber % 6 * 32),0,32,32)
                self.image = pg.transform.scale(self.image,(PLAYER_SIZE,PLAYER_SIZE))
                self.image.set_colorkey(BLACK)
                if self.playerlastDirection != 0:
                    self.image = pg.transform.flip(self.image, True, False)
                

    #gets image from Player sprite sheet
    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
       

    def collide_with_barrier(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x == (self.x + dx) and wall.y == self.y + dy:
                return True
        return False

    def UpdateBarrierColors(self,dx,dy):
        for wall in self.game.walls:
            if math.sqrt((((self.x/TILESIZE)-wall.x)**2)+(((self.y/TILESIZE)-wall.y)**2)) <= 4:
                wall.image = pg.image.load('GameAssets\\BoxDark3.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(TILESIZE,TILESIZE))
            elif math.sqrt((((self.x/TILESIZE)-wall.x)**2)+(((self.y/TILESIZE)-wall.y)**2)) <= 5:
                wall.image = pg.image.load('GameAssets\\BoxDark2.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(TILESIZE,TILESIZE))
            elif math.sqrt((((self.x/TILESIZE)-wall.x)**2)+(((self.y/TILESIZE)-wall.y)**2)) <= 6:
                wall.image = pg.image.load('GameAssets\\BoxDark.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(TILESIZE,TILESIZE))
            else:
                wall.image = pg.image.load('GameAssets\\BlackGround.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(TILESIZE,TILESIZE))

            #legacy code for box FOG OF WAR
            '''
            if abs(wall.x - (self.x + dx)) <= 4 and abs(wall.y - (self.y + dy))<= 4:
                wall.image = pg.image.load('GameAssets\\BoxDark3.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(32,32))
            elif abs(wall.x - (self.x + dx)) <= 8 and abs(wall.y - (self.y + dy))<= 8:
                wall.image = pg.image.load('GameAssets\\BoxDark2.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(32,32))
            elif abs(wall.x - (self.x + dx)) <= 12 and abs(wall.y - (self.y + dy))<= 12:
                wall.image = pg.image.load('GameAssets\\BoxDark.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(32,32))
            else:
                wall.image = pg.image.load('GameAssets\\BoxDark.png').convert_alpha()
                wall.image = pg.transform.scale(wall.image,(32,32))
            '''
            


    def move(self, dx=0, dy=0):
        if not self.collide_with_barrier(dx,dy):
            self.UpdateBarrierColors(dx,dy)
            self.x += dx
            self.y += dy

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.topleft = (self.x,self.y)
        '''
        adjusting for sprite size offset
        '''
        self.rect.y = self.rect.y + 13
        self.rect.x = self.rect.x + 25
        if not pg.sprite.spritecollideany(self,self.game.walls):
            self.UpdateBarrierColors(self.rect.x,self.rect.y)
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.x -= self.vx * self.game.dt
            self.y -= self.vy * self.game.dt
            self.rect.topleft = (self.x,self.y)
        else:
            self.rect.y = self.rect.y - 13
            self.rect.x = self.rect.x - 25


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.zlevel = 0
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.floorimage = pg.image.load('GameAssets\\BoxDark.png').convert_alpha()
        self.floorimage = pg.transform.scale(self.floorimage,(TILESIZE,TILESIZE))
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.image = self.floorimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Bg(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.zlevel = 0
        self.groups = game.all_sprites, game.bgs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.floorimage = pg.image.load('GameAssets\\BlackGround.png').convert_alpha()
        self.floorimage = pg.transform.scale(self.floorimage,(TILESIZE,TILESIZE))
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.image = self.floorimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE