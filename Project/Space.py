# This file will reproduce the software Space Asteroids, the game have an starship which will shoot at asteroids
# of different sizes which will give a score to the player. The player will have 5 lives to make the more score that he 
# can do, the score will be higher for shooting the smaller asteroids and lower for shooting the bigger ones. 
# The Object Oriented Programming principles used in this program were Abstractions, inheritence, encapsulation and polyphormism
# Some of the principles that can be find in this program are the heritance in the way that the some characteristic of some classes were inherited to other classes. 
# the program also used polyphormism to display the "score", "lives" and "play again" text in game.  
#
import pygame
import math
import random

pygame.init()

screen_w = 800
screen_h = 600

background = pygame.image.load('starbg.png')
starship = pygame.image.load('starship.png')
asteroid_a = pygame.image.load('asteroid50.png')
asteroid_b= pygame.image.load('asteroid100.png')
asteroid_c = pygame.image.load('asteroid150.png')

pygame.display.set_caption('Space Asteroids')

window = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()

game_over = False
lives = 5
score = 0

class Starship():
    def __init__(self):
        self.image = starship
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = screen_w//2
        self.y = screen_h//2
        self.angle = 0
        self.rotation1 = pygame.transform.rotate(self.image, self.angle)
        self.rotation2 = self.rotation1.get_rect()
        self.rotation2.center = (self.x, self.y)
        self.coseno = math.cos(math.radians(self.angle + 90)) 
        self.sen = math.sin(math.radians(self.angle + 90))
        self.front = (self.x + self.coseno * self.width // 2, self.y - self.sen * self.height // 2)


    def draw(self, window):  
         window.blit(self.rotation1, self.rotation2)
    
    def left_turn(self):
        self.angle += 5 
        self.rotation1 = pygame. transform.rotate(self.image, self.angle) 
        self.rotation2 = self.rotation1.get_rect()
        self.rotation2.center = (self.x, self.y)
        self.coseno = math.cos(math.radians(self.angle + 90))
        self.sen = math.sin(math.radians(self.angle + 90))
        self.front = (self.x + self.coseno * self.width // 2, self.y - self.sen * self.height // 2)

    def right_turn(self):
        self.angle -= 5 
        self.rotation1 = pygame. transform.rotate(self.image, self.angle) 
        self.rotation2 = self.rotation1.get_rect()
        self.rotation2.center = (self.x, self.y)
        self.coseno = math.cos(math.radians(self.angle + 90))
        self.sen = math.sin(math.radians(self.angle + 90))
        self.front = (self.x + self.coseno * self.width // 2, self.y - self.sen * self.height // 2)

    def forward(self):
        self.x += self.coseno * 6
        self.y -= self.sen * 6
        self.rotation1 = pygame. transform.rotate(self.image, self.angle) 
        self.rotation2 = self.rotation1.get_rect()
        self.rotation2.center = (self.x, self.y)
        self.coseno = math.cos(math.radians(self.angle + 90))
        self.sen = math.sin(math.radians(self.angle + 90))
        self.front = (self.x + self.coseno * self.width // 2, self.y - self.sen * self.height // 2)
    
    # Function to make starship appear keep appearing in bottom or top, left or right is player surpasses the borders 
    def location_check(self):
        if self.x > screen_w + 50:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = screen_w
        elif self.y < -50:
            self.y = screen_h
        elif self.y > screen_h + 50:
            self.y = 0

class Bullet():
    def __init__(self):
        self.point = starship.front
        self.x, self.y = self.point
        self.width = 4
        self.height = 4 
        self.cs = starship.coseno
        self.sn = starship.sen
        self.x_velocity = self.cs * 10
        self.y_velocity = self.sn * 10

    def movement(self):
        self.x += self.x_velocity
        self.y -= self.y_velocity

    def draw (self, window):
        pygame.draw.rect(window, (255, 255, 255), [self.x, self.y, self.width, self.height])
    
    def screen_check(self):
        if self.x < -50 or self.x > screen_w or self.y > screen_h or self.y < -50:
            return True

class Asteroids():
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid_a
        elif self.rank == 2:
            self.image = asteroid_b
        else:
            self.image = asteroid_c
        self.width = 50 * rank
        self.height = 50 * rank
        self.random_place = random.choice([(random.randrange(0, screen_w-self.width), random.choice([-1*self.height - 5, screen_h + 5])), (random.choice([-1*self.width - 5, screen_w + 5]), random.randrange(0, screen_h - self.height))])
        self.x, self.y = self.random_place
        if self.x < screen_w // 2:
            self.xdir = 1 
        else:
            self.xdir = -1
        if self.y < screen_h // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.x_velocity = self.xdir * random.randrange(1,3)
        self.y_velocity = self.ydir * random.randrange(1,3)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
    
def redraw_game_window():
    window.blit(background, (0,0))
    font = pygame.font.SysFont('agency FB', 25)   
    lives_text = font.render('Lives: ' + str(lives), 1, (0,255,0)) 
    play_again = font.render('Press space to play again', 1, (0, 255,0))
    score_points = font.render('Score: ' + str(score), 1, (0,255,0))
    starship.draw(window)
    for a in asteroids:
        a.draw(window) 
    for b in starship_bullets:
        b.draw(window)      

    if game_over: 
        window.blit(play_again,(screen_w //2 - play_again.get_width()//2, screen_h//2 - play_again.get_height()//2))
    window.blit(score_points, (screen_w - score_points.get_width() - 25, 25))
    window.blit(lives_text, (25, 25))
    pygame.display.update()

starship = Starship() 
starship_bullets = []
asteroids = []
count = 0
run = True
while run:
    clock.tick(60)
    count += 1
    if not game_over: 
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroids(ran))
    starship.location_check()
    for b in starship_bullets:
        b.movement()
        if b.screen_check():
            starship_bullets.pop (starship_bullets. index(b))

    for a in asteroids:
        a.x += a.x_velocity
        a.y += a.y_velocity

    # if starship hits an asteroid, the player will loose a life 
        if (starship.x >= a.x and starship.x <= a.x and a.width) or (starship.x + starship.width >= a.x and starship.x + starship.width <= a.x + a.width):
            if(starship.y >= a.y and starship.y <= a.y + a.height) or (starship.y + starship.height >= a.y and starship.y + starship.height <= a.y + a.height):
                lives -= 1
                asteroids.pop(asteroids. index(a))
                break


        # bullet hit asteroids
        for b in starship_bullets:
            if (b.x >= a.x and b.x <= a.x + a.width) or b.x + b.width >= a.x and b.x + b.width <= a.x + a.width:
                if (b.y >= a.y and b.y <= a.y + a.height) or b.y + b.height >= a.y and b.y + b.height <= a.y + a.height:
                    if a.rank == 3:
                        score += 10
                        new_ast1 = Asteroids(2)
                        new_ast2 = Asteroids(2)
                        new_ast1.x = a.x
                        new_ast2.x = a.x
                        new_ast1.y = a.y
                        new_ast2.y = a.y
                        asteroids.append(new_ast1)
                        asteroids.append(new_ast2)
                    elif a.rank == 2:
                        score += 20
                        new_ast1 = Asteroids(1)
                        new_ast2 = Asteroids(1)
                        new_ast1.x = a.x
                        new_ast2.x = a.x
                        new_ast1.y = a.y
                        new_ast2.y = a.y
                        asteroids.append(new_ast1)
                        asteroids.append(new_ast2)
                    else:
                        score += 30
                    asteroids.pop(asteroids.index(a))
                    starship_bullets.pop(starship_bullets.index(b))
        
        if lives <= 0:
            game_over = True

        keys = pygame.key.get_pressed()

        if keys[pygame. K_LEFT]:
            starship.left_turn()
        
        if keys[pygame. K_RIGHT]:
            starship.right_turn()
        if keys[pygame. K_UP]:
            starship.forward()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    starship_bullets.append(Bullet())
                else:
                    game_over = False
                    lives = 5
                    score = 0
                    asteroids.clear()


    redraw_game_window()

pygame.quit()


