import pygame
import math
import pygame.draw
import pygame.font
from random import randint
pygame.init()
pygame.font.init()

class Ball():
    def __init__(self, screen, color, position_x, position_y, radius, speed, direction):
        self.maxspeed = 10
        self.screen = screen
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.black_color = (0, 0, 0)
        
        self.alive = False
    def move(self):
        if (self.status()):
            pygame.draw.circle(self.screen, self.black_color, (self.position_x, self.position_y), self.radius)
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
                elif(possible_x + self.radius >1100):
                    self.direction = randint(int(math.pi),int(3/2*math.pi))
                else:
                    self.direction = randint(int(math.pi), int(2*math.pi))
            elif(possible_x - self.radius < 100):
                self.direction = randint(int(-math.pi/2),int(math.pi/2))
            elif(possible_x + self.radius > 1100):
                self.direction = randint(int(math.pi/2), int(3/2*math.pi))
                
            self.position_x = int(self.position_x + self.speed * math.cos(self.direction))
            self.position_y = int(self.position_y - self.speed * math.sin(self.direction))        
            pygame.draw.circle(self.screen, self.color, (self.position_x, self.position_y), self.radius)
        
    def status(self):
        return self.alive
    
    def birth(self):
        self.alive = True;
        self.color = (randint(50, 250), randint(50, 250), randint(50, 250))
        self.position_x = randint(100, 1100)
        self.position_y = randint(100, 800)
        self.radius = randint(10, 30)
        self.speed = randint(5, min([20, self.maxspeed]))
        self.direction = randint(-180, 180)
    
    def shot(self, point_x, point_y):
        if((point_x - self.position_x)**2 + (point_y - self.position_y)**2 < self.radius**2):
            self.alive = False
            pygame.draw.circle(self.screen, self.black_color, (self.position_x, self.position_y), self.radius)
            self.maxspeed += 1;
            return True
    
    def __del__(self):
        print("deaf")
    

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

font = pygame.font.SysFont(None, 100)
text = font.render('Score:', True, [255, 255, 255])
canvas.blit(text, [480, 0] )

balls = [0]*20
for i in range(20):
     balls[i] = Ball(canvas, COLORS[randint(0, 5)], randint(100, 1100), randint(100, 800), randint(10, 30), randint(5, 10), randint(-180, 180))
     
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
                        
    text = font.render('Score:' + str(score), True, [255, 255, 255])
    pygame.draw.line(canvas, BLACK, (0, 0), (1100, 0), 150)
    canvas.blit(text, [480, 0] )
    
    for ball in balls:
            ball.move()
    pygame.draw.line(canvas, RED, (100, 100), (1100, 100), 10)
    pygame.draw.line(canvas, RED,  (1100, 100), (1100, 800), 10)
    pygame.draw.line(canvas, RED, (1100, 800), (100, 800), 10)
    pygame.draw.line(canvas, RED, (100, 800), (100, 100), 10)
    pygame.display.update()
    if(time > 30):
        flag = True
        for ball in balls:
            if(ball.status() == False and flag == True):
                ball.birth()
                flag = False
        if(flag == True):
            print('game over')
            finished = True
        else:
            time = 0;
    time += 1;    

pygame.quit()

