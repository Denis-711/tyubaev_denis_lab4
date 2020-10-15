import pygame
import math
import pygame.draw
from random import randint
pygame.init()

class Ball():
    def __init__(self, screen, color, position_x, position_y, radius, speed, direction):
        self.screen = screen
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.speed = speed
        self.direction = direction
        self.black_color = (0, 0, 0)
        pygame.draw.circle(self.screen, self.color, (self.position_x, self.position_y), self.radius)
        self.alive = True
    def move(self):
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

def click(event):
    print(x, y, r)

pygame.display.update()
clock = pygame.time.Clock()
finished = False
color = COLORS[randint(0, 5)]

balls = [0]*4
for i in range(4):
     balls[i] = Ball(canvas, COLORS[randint(0, 5)], randint(300, 500), randint(300, 500), randint(10, 50), randint(2,10), randint(-180, 180))
     
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
            click(event)
    for ball in balls:
            ball.move()
    pygame.draw.line(canvas, RED, (100, 100), (1100, 100), 10)
    pygame.draw.line(canvas, RED,  (1100, 100), (1100, 800), 10)
    pygame.draw.line(canvas, RED, (1100, 800), (100, 800), 10)
    pygame.draw.line(canvas, RED, (100, 800), (100, 100), 10)
    pygame.display.update()    

pygame.quit()

