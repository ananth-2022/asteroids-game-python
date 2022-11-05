import pygame as pg
import random

pg.init()
window = pg.display.set_mode((800, 800))
font = pg.font.SysFont(None, 25)
clock = pg.time.Clock()
## CONSTANTS
BULLET_VELOCITY = pg.math.Vector2(8, 0)
BULLET_LIFE = 0.75*60
##
sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
ships = pg.sprite.Group()
asteroids = pg.sprite.Group()

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, radius, angle, velocity):
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.angle = angle
        self.radius = radius
        self.velocity = BULLET_VELOCITY.rotate(self.angle-90)+velocity
        self.time_existed = 0
        self.image = pg.Surface([self.radius+1, self.radius+1])
        self.image.fill("black")
        pg.draw.circle(self.image, "red", (self.radius/2, self.radius/2), self.radius/2)
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y
    
    def wraparound(self):
        if self.position.x >= 800:
            self.position.x = 0
        elif self.position.x <= 0:
            self.position.x = 800
        if self.position.y >= 800:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = 800 
    
    def update(self):
        if self.time_existed >= BULLET_LIFE:
            self.kill()
        self.time_existed+=1
        self.position += self.velocity
        self.wraparound()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

class Ship(pg.sprite.Sprite):
    def __init__(self, width, height, position):
        pg.sprite.Sprite.__init__(self)
        self.width = width
        self.angle = 0
        self.velocity = pg.Vector2(0, 0)
        self.position = position
        self.lives = 3
        self.image = pg.Surface([width+1, height+1])
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.bullet_timer = 0
    
    def drawlines(self):
        self.image.fill("black")
        p1 = pg.math.Vector2(20,0).rotate(self.angle-90)+pg.math.Vector2(25,25)
        p2 = pg.math.Vector2(25,0).rotate(self.angle+120-90)+pg.math.Vector2(25,25)
        p3 = pg.math.Vector2(25,0).rotate(self.angle+240-90)+pg.math.Vector2(25,25)
        pg.draw.lines(self.image, "white", True, [p1, p2, p3])
    
    def wraparound(self):
        if self.position.x >= 800:
            self.position.x = 0
        elif self.position.x <= 0:
            self.position.x = 800
        if self.position.y >= 800:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = 800 
    
    def shoot(self):
        b = Bullet(pg.math.Vector2(self.position.x + 25, self.position.y + 25), 5, self.angle, self.velocity.copy())
        sprites.add(b)
        bullets.add(b)
    
    def update(self):
        if pg.sprite.spritecollide(self, asteroids, False):
            self.lives -= 1
            self.position = pg.math.Vector2(400, 400)
            self.angle = 0
            self.velocity = pg.math.Vector2(0,0)
        if self.lives < 1:
            self.kill()
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.angle -= 5
        if keys[pg.K_d]:
            self.angle += 5
        if keys[pg.K_w]:
            self.velocity += pg.Vector2(1/6, 0).rotate(self.angle-90)
        if keys[pg.K_SPACE]:
            self.shoot()
        self.position += self.velocity
        self.wraparound()
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.drawlines()

class Asteroid(pg.sprite.Sprite):
    def __init__(self, size, position):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        if self.size == 3:
            self.radius = 100
        if self.size == 2:
            self.radius = 50
        if self.size == 1:
            self.radius = 20
        self.position = position
        self.velocity = pg.math.Vector2(1, 0).rotate(random.randint(0,360))
        self.image = pg.Surface([self.radius+1, self.radius+1])
        self.image.fill("black")
        pg.draw.circle(self.image, (140, 140, 140), (self.radius/2, self.radius/2), self.radius/2)
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y
    
    def wraparound(self):
        if self.position.x >= 800:
            self.position.x = 0
        elif self.position.x <= 0:
            self.position.x = 800
        if self.position.y >= 800:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = 800 
    
    def update(self):
        if pg.sprite.spritecollide(self, bullets, True):
            self.kill()
            if self.size >= 2:
                a1 = Asteroid(self.size -1, self.position.copy())
                a2 = Asteroid(self.size -1, self.position.copy())
                sprites.add(a1)
                sprites.add(a2)
                asteroids.add(a1)
                asteroids.add(a2)
        self.position += self.velocity
        self.wraparound()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

def spawn_asteoids(l):
    for i in range(l+2):
        a = Asteroid(3, pg.math.Vector2(random.randint(0,800), random.randint(0, 800)))
        sprites.add(a)
        asteroids.add(a)

def game():
    level = 1
    player = Ship(50, 50, pg.math.Vector2(400, 400))
    sprites.add(player)
    ships.add(player)
    spawn_asteoids(level)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        
        if not asteroids:
            level += 1
            spawn_asteoids(level)
        asteroids_left = font.render(f'Asteroids left = {len(asteroids)}', True, 'white')
        lives_left = font.render(f'Lives = {player.lives}', True, 'white')
        level_label = font.render(f'Level {level}', True, "white")
        sprites.update()
        window.fill("black")
        window.blit(asteroids_left, (10, 10))
        window.blit(lives_left, (650, 10))
        window.blit(level_label, (400, 10))
        sprites.draw(window)
        if not player.alive():
            game_over = font.render('GAME OVER!! press r to restart', True, "red")
            window.blit(game_over, (400, 400))
            if pg.key.get_pressed()[pg.K_r]:
                game()
        pg.display.flip()
        clock.tick(60)

game()