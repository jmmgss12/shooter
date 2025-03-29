#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < W - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W-80)
            lost += 1

class Rock(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W-80)


            

H = 500
W = 700
main_win = display.set_mode((W, H))
display.set_caption('Шутер')
back = transform.scale(image.load('galaxy.jpg'), (W, H))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(1)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

ship = Player('rocket.png', W//2, H-110, 80, 100, 5)
ufos = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', randint(80, W-80), -40, 80, 50, randint(1, 3))
    ufos.add(ufo)
asteroids = sprite.Group()
for d in range(2):
    asteroid = Rock('asteroid.png', randint(80, W-80), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()

clock = time.Clock()
FPS = 60

score = 0
lost = 0
hp = 100

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)
win = font2.render('YOU WIN!', True, (255, 215, 0))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if finish != True:
        main_win.blit(back, (0, 0))

        ship.update()
        ufos.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        ufos.draw(main_win)
        asteroids.draw(main_win)
        bullets.draw(main_win)


        if lost >= 10:
            main_win.blit(lose, (W//2 - 80, H//2 - 20))
            finish = True

        if sprite.spritecollide(ship, ufos, True):
            hp -= 25
            # main_win.blit(lose, (W//2 - 80, H//2 - 20))


        if sprite.spritecollide(ship, asteroids, True):
            # main_win.blit(lose, (W//2 - 80, H//2 - 20))
            hp -= 25

        collides = sprite.groupcollide(bullets, ufos, True, True)
        for f in collides:
            score += 1
            ufo = Enemy('ufo.png', randint(80, W-80), -40, 80, 50, randint(1, 3))
            ufos.add(ufo)

        collides = sprite.groupcollide(bullets, asteroids, True, False)


        if hp <= 0:
            main_win.blit(lose, (W//2 - 80, H//2 - 20))
            finish = True


        
        text_score = font1.render("Счет: " +str(score), 1, (255, 255, 255))
        text_lost = font1.render("Пропущено: " +str(lost), 1, (255, 255, 255))
        text_hp = font1.render("Здоровье: " +str(hp), 1, (255, 255, 255))
        main_win.blit(text_score, (10, 20))
        main_win.blit(text_lost, (10, 50))
        main_win.blit(text_hp, (10, 80))

        # if score >= 10:
        #     main_win.blit(win, (W//2 - 80, H//2 - 20))
        #     finish = True

            

        display.update()
    clock.tick(FPS)

