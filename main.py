from pygame import *
from random import randint
import os
font.init()
mixer.init()

path1 = os.path.join(os.getcwd(), "space")

window = display.set_mode((700, 500))
background = os.path.join(path1, "galaxy.jpg")
background = image.load(background)

player_image = os.path.join(path1, "rocket.png")
player_image = image.load(player_image)

enemy_img = os.path.join(path1, "ufo.png")
enemy_img = image.load(enemy_img)

bullet_img = os.path.join(path1, "bullet.png")
bullet_img = image.load(bullet_img)

backsound = os.path.join(path1, "space.ogg")

fire_ogg = os.path.join(path1, "fire.ogg")
fire_ogg = mixer.Sound(fire_ogg)

boom = os.path.join(path1, "bom.ogg")
boom = mixer.Sound(boom)

win = os.path.join(path1, "win.ogg")
win = mixer.Sound(win)

lose = os.path.join(path1, "lose.ogg")
lose = mixer.Sound(lose)

Icone = os.path.join(path1, "icon.bmp")
Icone = image.load(Icone)
display.set_icon(Icone)

mixer.init()
mixer.music.load(backsound)
mixer.music.play()

background = transform.scale(background, (700, 500))
display.set_caption('Space')
game = True
FPS = 60
clock = time.Clock()

def set_value():
    global points
    points += 1
points = -1
set_value()
balls = 0
def set_true():
    global balls
    balls += 1
balls = -1
set_true()

def end():
    global end
    end += 1  
end = 0

def move():
    global move
    move += 1
move = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.width = width
        self.height = height
        
        self.player_image = transform.scale(player_image, (width, height))
        self.speed = player_speed
        self.rect = self.player_image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.player_image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
    def update(self):
        if (key.get_pressed()[K_a] or key.get_pressed()[K_LEFT]) and self.rect.x > -5:
            self.rect.x -= self.speed
            '''if self.le_ra <= 1:
                self.image = transform.flip(self.image, True, False)
                self.le_ra = 2'''
        if (key.get_pressed()[K_d] or key.get_pressed()[K_RIGHT]) and self.rect.x < 640:
            self.rect.x += self.speed
            '''if self.le_ra >= 2:
                self.image = transform.flip(self.image, True, False)
                self.le_ra = 1'''
    def fire(self):
        bul = Bullet(bullet_img, player.rect.centerx - 2, player.rect.top, 6, 10, 20)
        player.bullets.append(bul)
        fire_ogg.play()
    
    def touch(self, group):
        global points
        if end == 0:
            collided = sprite.spritecollide(self, group, False)
            if collided:
                boom.play()
                points += 20


class Enemy(GameSprite): 
    def move(self):
        self.rect.y += randint(1, 5)
        if self.rect.y >= 500:
            self.rect.x = randint(0, 600)
            self.rect.y = -60
            set_value()
                                                                        
class Bullet(GameSprite):                                         
    def move(self):                                        
        self.rect.y -= self.speed
        if self.rect.y <= -self.rect.height:
            player.bullets.remove(self)      
    def hit(self, group):
        if end == 0:
            collided = sprite.spritecollide(self, group, False)
            if collided:
                boom.play()
                for gr in collided:
                    gr.rect.x = randint(0, 600)
                    gr.rect.y = -60
                self.remove()
                player.bullets.remove(self)     
                set_true()
                                                              
def numbers(text1, shirina, x_cord, y_cord, color, txt):                              
    f1 = font.SysFont("Arial", shirina)                                             
    text1 = f1.render(txt + str(text1), True, (color))                           
    window.blit(text1, (x_cord, y_cord))                               
                                                                                                                               
player = Player(player_image, 300, 400, 8, 64, 80)                     
player.bullets = []                                                             
                                                        
#Список врагов                                                    
enemies = []                                                   
for i in range(5):                                                     
    enemy = Enemy(enemy_img, randint(0, 600), -100, randint(1,5), 64, 128)
                                                                       
    enemies.append(enemy)


def reset_game(enemies):
    global points
    global balls
    global end
    global move
    end = 0
    balls = 0
    points = 0
    move = 0
    for gr1 in enemies:
        gr1.rect.x = randint(0, 600)
        gr1.rect.y = -60



        
    

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    window.blit(background, (0,0))
    player.reset()
    player.update()
    player.touch(enemies)
    for bu in player.bullets:
        bu.reset()
        bu.move()
        bu.hit(enemies)
    if move == 0:
        for en in enemies:
            en.reset()
            en.move()
        numbers(str(balls), 50, 25, 25, (180, 0, 0), 'Очков ')
        numbers(str(points), 50, 25, 60, (180, 0, 0), 'Пропущено ')
        if balls >= 30 or points >= 5:
            move += 1
            
    elif move == 1 and balls >= 30:
        if end == 0:
            win.play() 
            mixer.music.stop()
            end += 1  
        if key.get_pressed()[K_UP] == True:
            reset_game(enemies )
        numbers('выиграли!', 100, 100, 200, (180, 0, 0), 'Вы ')
        numbers('чтобы начать заново!', 38, 10, 300, (180, 0, 0), 'Нажмите стрелку вверх, ')
    elif move == 1 and points >= 5:
        if end == 0:
            lose.play() 
            mixer.music.stop()
            end += 1  
        if key.get_pressed()[K_UP] == True:
            reset_game(enemies)
        numbers('проиграли!', 100, 100, 200, (180, 0, 0), 'Вы ')
        numbers('чтобы начать заново!', 38, 10, 300, (180, 0, 0), 'Нажмите стрелку вверх, ')
    display.update()
    clock.tick(FPS)