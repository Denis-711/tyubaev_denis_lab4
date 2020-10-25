import pygame
import math
import pygame.draw
import pygame.font
from random import randint
pygame.init()
pygame.font.init()

class Base_Target():
    def __init__(self, screen):
        self.maxspeed = 20
        self.screen = screen
        self.color = (randint(50, 255), randint(50, 255), randint(50, 255))
        self.position_x = randint(200, 1000)
        self.position_y = randint(200, 700)
        self.speed = randint(5, 10)
        self.direction = randint( -180, 180)
        self.radius = randint(15, 25)
        self.alive = False
        
    def change_coordinates(self):
        if (self.status()):
            possible_x = int(self.position_x + self.speed * math.cos(self.direction))
            possible_y = int(self.position_y - self.speed * math.sin(self.direction))
            if(possible_y + self.radius > 800):
                if(possible_x - self.radius < 100):
                    self.direction = randint(0, int(math.pi/2))
                elif(possible_x + self.radius > 1100):
                    self.direction = randint(int(math.pi/2),int(math.pi))
                else:
                    self.direction = randint(0, int(math.pi))
            elif(possible_y - self.radius < 100):
                if(possible_x - self.radius < 100):
                    self.direction = randint(int(3/2*math.pi), int(2*math.pi))
                elif(possible_x + self.radius > 1100):
                    self.direction = randint(int(math.pi),int(3/2*math.pi))
                else:
                    self.direction = randint(int(math.pi), int(2*math.pi))
            elif(possible_x - self.radius < 100):
                self.direction = randint(int(-math.pi/2),int(math.pi/2))
            elif(possible_x + self.radius > 1100):
                self.direction = randint(int(math.pi/2), int(3/2*math.pi))
            self.position_y = int(self.position_y - self.speed * math.sin(self.direction))   
            self.position_x = int(self.position_x + self.speed * math.cos(self.direction))
    def rebirth(self):
        self.alive = True
        self.position_x = randint(200, 1000)
        self.position_y = randint(200, 700)
        self.radius = randint(15, 25)
        self.speed = randint(5, min([20, self.maxspeed]))
        self.direction = randint(-180, 180)
    
    def status(self):
        return self.alive		
		

class Ball(Base_Target):
    def __init__(self, screen):
        super().__init__(screen)
        self.black_color = (0, 0, 0)
        self.alive = False

    def move(self):
        if(self.status()):
            pygame.draw.circle(self.screen, self.black_color, (self.position_x, self.position_y), self.radius)
            self.change_coordinates()
            pygame.draw.circle(self.screen, self.color, (self.position_x, self.position_y), self.radius)
    
    def shot(self, point_x, point_y):
        if((point_x - self.position_x)**2 + (point_y - self.position_y)**2 < self.radius**2 and self.alive == True):
            self.alive = False
            pygame.draw.circle(self.screen, self.black_color, (self.position_x, self.position_y), self.radius)
            self.maxspeed += 1;
            return True	
    
    def __del__(self):
        print("deaf")

class Square(Base_Target):
    def __init__(self, screen):
        super().__init__(screen)
        self.black_color = (0, 0, 0)
        self.alive = False
        self.color = (0, 255, 0)
                
    def move(self):
        if(self.status()):
            pygame.draw.rect(self.screen, self.black_color, (self.position_x, self.position_y, self.radius, self.radius))
            pygame.draw.rect(self.screen, self.black_color, (self.position_x, self.position_y, self.radius, self.radius), 4)
            self.change_coordinates()
            pygame.draw.rect(self.screen, self.color, (self.position_x, self.position_y, self.radius, self.radius))
            pygame.draw.rect(self.screen, (255, 0, 0), (self.position_x, self.position_y, self.radius, self.radius), 4)             
            
    def shot(self, point_x, point_y):
        if(abs(point_x - self.position_x) < self.radius and abs(point_y - self.position_y) < self.radius and self.alive == True):
            self.alive = False
            pygame.draw.rect(self.screen, self.black_color, (self.position_x, self.position_y, self.radius, self.radius))
            pygame.draw.rect(self.screen, self.black_color, (self.position_x, self.position_y, self.radius, self.radius), 4)
            self.maxspeed += 1;
            return True
        elif ((abs(point_x - self.position_x) < 3 * self.radius and abs(point_y - self.position_y) < 3 * self.radius and self.alive == True)):
            pygame.draw.rect(self.screen, self.black_color, (self.position_x, self.position_y, self.radius, self.radius))
            pygame.draw.rect(self.screen, self.black_color, (self.position_x, self.position_y, self.radius, self.radius), 4)
            self.position_x = randint(200, 1000)
            self.position_y = randint(200, 700)
            self.direction = randint(-180, 180)		
        
    
FPS = 30
canvas = pygame.display.set_mode((1200, 900))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
pygame.display.update()
clock = pygame.time.Clock()
finished = False
color = COLORS[randint(0, 5)]
score = 0
time = 0
time1 = 0
font = pygame.font.SysFont(None, 100)
text = font.render('Score:', True, [255, 255, 255])
canvas.blit(text, [480, 0] )
balls = [0]*20

for i in range(20):
     balls[i] = Ball(canvas)
     
square = Square(canvas)
     
pygame.draw.line(canvas, RED, (100, 100), (1100, 100), 10)
pygame.draw.line(canvas, RED,  (1100, 100), (1100, 800), 10)
pygame.draw.line(canvas, RED, (1100, 800), (100, 800), 10)
pygame.draw.line(canvas, RED, (100, 800), (100, 100), 10)
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            for ball in balls:
                if (ball.status):
                    x, y = event.pos
                    if(ball.shot(x, y)):
                        score += 1;
            if(square.status):
                x, y = event.pos
                if(square.shot(x,y)):
                    score += 10
                        
    text = font.render('Score:' + str(score), True, [255, 255, 255])
    pygame.draw.line(canvas, BLACK, (0, 0), (1100, 0), 150)
    canvas.blit(text, [480, 0] )
    
    square.move()    
    for ball in balls:
        ball.move()
    pygame.draw.line(canvas, RED, (100, 100), (1100, 100), 10)
    pygame.draw.line(canvas, RED,  (1100, 100), (1100, 800), 10)
    pygame.draw.line(canvas, RED, (1100, 800), (100, 800), 10)
    pygame.draw.line(canvas, RED, (100, 800), (100, 100), 10)
    pygame.display.update()
    if(time > 30):
        flag = True
        flag1 = True
        for ball in balls:
            if(ball.status() == False and flag == True):
                ball.rebirth()
                flag = False
        if(flag == True):
            print('game over')
            finished = True
        else:
            time = 0
    if(time1 > 270):
        if(square.status() == False and flag1 == True):
            if(square.status() == False and flag1 == True):
                square.rebirth()
                flag1 = False
        time1 = 0
    time += 1
    time1 += 1    
pygame.quit()
