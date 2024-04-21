from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

img_back = "dsBuffer.bmp.png"
img_hero = "specnaz.png"
img_enemy = "pngegg.png"
img_asteroid = "1234-transformed.png"
img_bullet = "bullet.png"  # Додана змінна для шляху до картинки кулі

score = 0
lost = 0
goal = 100
max_lost = 10
life = 3


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (size_x, size_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery - 10, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = win_width
            self.rect.y = randint(80, win_height - 80)


class Asteroid(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = win_width
            self.rect.y = randint(80, win_height - 80)


class Bullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # Оригінальна ширина картинки, щоб врахувати її при розгортанні хітбоксу
        self.original_width = self.rect.width

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > win_width:
            self.kill()

    def reset(self):
        # Розгортаємо хітбокс вправо
        self.rect = self.image.get_rect()
        self.rect.x = self.original_width
        self.rect.y = self.rect.y


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 20, win_height // 2, 80, 100, 10)  # Adjusted the x position of the ship.

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, win_width + randint(50, 200), randint(80, win_height - 80), 80, 50, randint(1, 3))
    monsters.add(monster)

for i in range(1, 3):
    asteroid = Asteroid(img_asteroid, win_width + randint(50, 200), randint(80, win_height - 80), 80, 50, randint(1, 3))
    asteroids.add(asteroid)

run = True
finish = False
clock = time.Clock()
FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy(img_enemy, win_width + randint(50, 200), randint(80, win_height - 80), 80, 50,
                            randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if lost >= max_lost or life == 0:
            finish = True
            window.blit(lose, (200, 200))

        text = font1.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render("Lost: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font1.render("Life: " + str(life), 1, (0, 150, 0))
        window.blit(text_life, (10, 10))  # Adjusted the x position of the life text.

        display.update()

    clock.tick(FPS)
