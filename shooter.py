from pygame import*
from random import randint
from time import time as timer

win = display.set_mode(((700, 500)))
display.set_caption('shooter')
background = transform.scale(image.load('D://pycharm progects//shooter//galaxy.jpg'),(700, 500))

lost = 0
score = 0


font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',50)
win2 = font2.render('YOU WIN!',True,(0,255,0))
lose = font2.render('YOU LOSE!',True,(255,0,0))

class GameSprite(sprite.Sprite):
    def __init__(self,img,speed,x,y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image,self.rect)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('D://pycharm progects//shooter//bullet.png',15,self.rect.centerx,self.rect.top,15,20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(80,620)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('D://pycharm progects//shooter//space.ogg')
mixer.music.play()
bullet_sound = mixer.Sound('D://pycharm progects//shooter//fire.ogg')

player = Player('D://pycharm progects//shooter//rocket.png',10,5,400,80,100)
monsters = sprite.Group()
for m in range(5):
    monster = Enemy('D://pycharm progects//shooter//ufo.png',randint(1,2),randint(80,620),0,80,50)
    monsters.add(monster)

asteroids = sprite.Group()
for a in range(2):
    asteroid = Asteroid('D://pycharm progects//shooter//asteroid.png',1,randint(80,620),0,80,50)
    asteroids.add(asteroid)

bullets = sprite.Group()


game = True
finish = False
life = 3
clock = time.Clock()
FPS = 60
# bessmertie =

bullets_num = 0
reload_time = False

while game :
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullets_num < 5 and reload_time == False:
                    bullets_num +=1
                    player.fire()
                    bullet_sound.play()
                if bullets_num >= 5 and reload_time == False:
                    last_bull = timer()
                    reload_time  = True

    if not finish:
        ts = font1.render('Сбито: '+ str(score),True,(255,255,255))
        tl = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        win.blit(background, (0, 0))
        win.blit(ts,(10,20))
        win.blit(tl, (10, 50))
        bullets.update()
        bullets.draw(win)
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(win)
        asteroids.update()
        asteroids.draw(win)
        sprite.groupcollide(asteroids, bullets, False, True)
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for i in collides:
            score += 1
            monster = Enemy('D://pycharm progects//shooter//ufo.png', randint(1, 2), randint(80, 620), 0, 80, 50)
            monsters.add(monster)

        if score >= 20:
            finish = True
            win.blit(win2,(200,200))

        if sprite.spritecollide(player,monsters,False) or lost >= 3 or sprite.spritecollide(player,asteroids,False):
            life -= 1
#           if life = :




        if lost >= 10 or life == 0:
            finish =True
            win.blit(lose,(200,200))


        text_life = font2.render(str(life), 1, (255, 255, 255))
        win.blit(text_life, (650, 0))

        if reload_time == True:
            now_time = timer()

            if now_time - last_bull <3:
                reload = font1.render('Перезарядка',1,(255,0,0))
                win.blit(reload,(250,450))
            else:
                reload_time = False
                bullets_num = 0


    display.update()
    clock.tick(FPS)


































