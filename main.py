from pygame import *
from random import randint
from time import time as timer

font.init()
FOOnt = font.SysFont("Arial",35)
fonttttt = font.SysFont("Arial",35)
fot = font.SysFont("Arial",35)
win = display.set_mode((700,500))
win_height = 500
win_width = 700
display.set_caption("Шутер")
bckgrnd = transform.scale(image.load("galaxy.jpg"),(700,500))
win.blit(bckgrnd,(0,0))



class GameSprite(sprite.Sprite):
    def __init__ (self,rocket_image,rocket_x,rocket_y,size_x,size_y,rocket_speed):
        super().__init__()
        self.image = transform.scale(image.load(rocket_image),(size_x,size_y))
        self.rocket_speed = rocket_speed
        self.rect = self.image.get_rect()
        self.rect.y = rocket_y
        self.rect.x = rocket_x
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))



class Rocket(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.rocket_speed  
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.rocket_speed
        

    def fire(self):        
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.rocket_speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(100,600)
            global lost
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.rocket_speed
        if self.rect.y < 0:
            self.kill()


spaceship = Rocket("rocket.png",5,win_height - 100,80,100,10)
FPS = 60
run = True
finish = False
clock = time.Clock()    

rel_time = False
num_fire = 0 
            
bullets = sprite.Group()
asteroids = sprite.Group()           

monsters = sprite.Group()
for i in range(5):
    monster1 = Enemy("ufo.png",randint(100,600),40,80,50,randint(1,3))
    monsters.add(monster1)
for i in range(3):
    asteroid = Enemy("asteroid.png",randint(100,600),40,80,50,randint(1,3))
    asteroids.add(asteroid)
    
score = 0
lifes = 3

while run:
    for i in event.get():
        if i .type == QUIT:
            run = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire <5 and rel_time == False:
                    spaceship.fire()
                    num_fire += 1
                if num_fire >=5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
            

    if not finish:
        win.blit(bckgrnd,(0,0)) 
      
        
        spaceship.update()
        monsters.update()
        spaceship.reset()  
        monsters.draw(win)
        bullets.update()   
        bullets.draw(win)
        asteroids.update()
        asteroids.draw(win)
        if lost > 3:
            finish = True
            
   
        if score > 10:
            finish = True
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = fot.render("Wait,reload",1,(255,0,0))
                win.blit(reload_text,(400,350))

   
        asteroid_collide = sprite.spritecollide(spaceship,asteroids, True)
        monster_collide = sprite.spritecollide(spaceship,monsters, True)
        bullets_collide = sprite.groupcollide(monsters,bullets,True,True)
        for s in bullets_collide:
            monster1 = Enemy("ufo.png",randint(100,600),40,80,50,randint(1,2))
            score = score + 1
            monsters.add(monster1)
        for life in asteroid_collide:
            asteroid = Enemy("asteroid.png",randint(100,600),40,80,50,randint(1,3))
            lifes = lifes - 1
            asteroids.add(asteroid)
        
        
        text_score = fonttttt.render("Счет:" + str(score),1,(255,255,255))
         
        text_lost = FOOnt.render("Пропущено:" + str(lost),1,(255,255,255)) 
        win.blit(text_score,(10,10))
        win.blit(text_lost,(10,40))
        
    display.update()
    clock.tick(FPS)
