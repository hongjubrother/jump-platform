# Sprite classes for platform game


from settings import *
import pygame as pg
vec = pg.math.Vector2 
# 2차원 벡터 클래스 (위치, 속도, 가속도 표현하고 조작 가능)
# 게임 객체의 이동, 충돌 감지, 힘 및 방향 계산 들을 구현할 수 있다.

class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
            # grap on  imamge out of a larger spritesheet
            image = pg.Surface((width,height))
            image.blit(self.spritesheet, (0,0), (x, y, width, height))
            image.pg.transform.scale(image, (width//2, height//2))
            return image
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0 # ex) 걷는 모션은 2프레임
        self.last_update = 0 
        self.load_images() #한번에 묶기
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2 , HEIGHT /2)
        self.pos = vec(WIDTH/2, HEIGHT/2)# 객체의 위치를 나타내는 변수
        self.vel = vec(0, 0)# vel = 속도, 초기 속도 0 , 정지를 의미
        self.acc = vec(0, 0) # acc = 가속도 , 초기 가속도 0으로 설정

    def load_images(self): 
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191), 
                                self.game.spritesheet.get_image(690, 406, 120, 201)]
        for frame in self.standing_frames:
                frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120,201), 
                                self.game.spritesheet.get_image(692, 1458, 120, 207)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = [self.game.spritesheet.get_image(382, 763, 150, 181)]
        self.jump_frame.set_colorkey(BLACK)
    
    def jump(self):
        
        # jump only if standing
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -40



    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV) 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: 
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]: 
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #wrap around the side of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos

    def animate(self): #프레임 부분(캐릭터 움직이는 애니메이션)
        now  = pg.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y






