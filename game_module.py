import pygame
import math
import pygame.draw
import pygame.font
from random import randint


class Base_Target():
	
    def __init__(self, screen, screen_widht, screen_height):
        '''
		
		Keyword argument:
		screen_widht -- game window width
		screen_height -- game window height
		'''
        self.spawn_x_min = 200
        self.spawn_x_max = screen_widht - 200
        self.spawn_y_min = 200
        self.spawn_y_max = screen_height - 200
        self.maxspeed = 20
        self.screen = screen
        self.color = (randint(50, 255), randint(50, 255), randint(50, 255))
        self.position_x = randint(self.spawn_x_min, self.spawn_x_max)
        self.position_y = randint(self.spawn_y_min, self.spawn_y_max)
        self.speed = randint(5, 10)
        self.direction = randint( -180, 180)
        self.radius = randint(15, 25)
        self.alive = False
        
    def change_coordinates(self):
        '''
        Function changes the coordinates of the target,
        moving evenly and progressively and interacting with the walls.
        '''
        if (self.status()):
            dx = self.speed * math.cos(self.direction)
            dy =  -1.0 * self.speed * math.sin(self.direction)
            possible_x = int(self.position_x + dx)
            possible_y = int(self.position_y + dy)
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
            dy = -1.0 * self.speed * math.sin(self.direction)
            dx =  self.speed * math.cos(self.direction)
            self.position_y = int(self.position_y + dy)   
            self.position_x = int(self.position_x + dx)

    def rebirth(self):
        '''
        Function activates an inactive target.
        '''
        self.alive = True
        self.position_x = randint(self.spawn_x_min, self.spawn_x_max)
        self.position_y = randint(self.spawn_y_min, self.spawn_y_max)
        self.radius = randint(15, 25)
        self.speed = randint(5, min([20, self.maxspeed]))
        self.direction = randint(-180, 180)
        if(type(self) == Ball):
            self.color = (randint(50, 255), randint(50, 255), randint(50, 255))
    
    def status(self):
        '''
        Function tells whether target is active
        '''
        return self.alive


class Ball(Base_Target):
    def __init__(self, screen, screen_widht, screen_height):
        super().__init__(screen, screen_widht, screen_height)
        self.black_color = (0, 0, 0)
        self.alive = False

    def move(self):
        '''
        Function moves the ball across the screen.
        '''
        if(self.status()):
            pygame.draw.circle(self.screen, self.black_color,
                               (self.position_x, self.position_y), self.radius)
            self.change_coordinates()
            pygame.draw.circle(self.screen, self.color,
                               (self.position_x, self.position_y), self.radius)
    
    def shot(self, point_x, point_y):
        '''
        Function checks if there is an intersection between the ball
        and the point transmitted by the coordinates,
        and if there is, it deactivates the ball.
        
        Keyword arguments:
        point_x -- x coordinate of the click
        point_y -- y coordinate of the click
        '''
        dist = (point_x - self.position_x)**2 + (point_y - self.position_y)**2
        if(dist < self.radius**2 and self.alive == True):
            self.alive = False
            pygame.draw.circle(self.screen, self.black_color,
                               (self.position_x, self.position_y), self.radius)
            self.maxspeed += 1;
            return True	
    


class Square(Base_Target):

    def __init__(self, screen, screen_widht, screen_height):
        super().__init__(screen, screen_widht, screen_height)
        self.black_color = (0, 0, 0)
        self.alive = False
        self.color = (0, 255, 0)
        self.red = (255, 0, 0)
                
    def move(self):
        '''
        Function moves the square across the screen.
        '''
        if(self.status()):
            pygame.draw.rect(
                self.screen, self.black_color,
                (self.position_x, self.position_y, self.radius, self.radius)
                )
            pygame.draw.rect(
                self.screen, self.black_color,
                (self.position_x, self.position_y, self.radius, self.radius), 4
                )
            self.change_coordinates()
            pygame.draw.rect(
                self.screen, self.color,
                (self.position_x, self.position_y, self.radius, self.radius)
                )
            pygame.draw.rect(self.screen, self.red,
            (self.position_x, self.position_y, self.radius, self.radius), 4)             
            
    def shot(self, point_x, point_y):
        '''
        Function checks if there is an intersection between the ball
        and the point transmitted by the coordinates,
        and if there is, it deactivates the ball.
        If the player clicked close to the square, but did not hit it,
        then the square teleports
        and changes the speed and direction of movement.
        
        Keyword arguments:
        point_x -- x coordinate of the click
        point_y -- y coordinate of the click
        '''
		
        if(abs(point_x - self.position_x) < self.radius and
           abs(point_y - self.position_y) < self.radius and
           self.alive == True):
            self.alive = False
            pygame.draw.rect(
                self.screen, self.black_color,
                (self.position_x, self.position_y, self.radius, self.radius)
                )
            pygame.draw.rect(
                self.screen, self.black_color,
                (self.position_x, self.position_y, self.radius, self.radius), 4
                )
            self.maxspeed += 1;
            return True
        elif ((abs(point_x - self.position_x) < 3 * self.radius and
              abs(point_y - self.position_y) < 3 * self.radius and
              self.alive == True)):
            pygame.draw.rect(
                self.screen, self.black_color,
                (self.position_x, self.position_y, self.radius, self.radius)
                )
            pygame.draw.rect(
                self.screen, self.black_color,
                (self.position_x, self.position_y, self.radius, self.radius), 4
                )
            self.position_x = randint(self.spawn_x_min, self.spawn_x_max)
            self.position_y = randint(self.spawn_y_min, self.spawn_y_max)
            self.direction = randint(-180, 180)


class Act():
	
    def __init__(self):
        pygame.init()
        pygame.font.init()
        # technical constants that do not affect gameplay(dont change)
        self.flag = True
        self.flag1 = True
        self.finished = False
        self.clock_ball = 0 
        self.clock_square = 0
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.score = 0
	    # parameters responsible for the appearance of the game(changable)
        self.fps = 30
        self.screen_height = 900
        self.screen_widht = 1200    
        # parameters determining the difficulty of the game(changable)
        self.max_balls_amount = 20 # game overs if number of balls exceeds
        self.spawn_period_ball = 30 # time of appearance of a new ball
        self.spawn_period_square = 270 # time of appearance of a new square

    def setting(self):
        self.balls = [0] * self.max_balls_amount
        self.canvas = pygame.display.set_mode((self.screen_widht, 
                                              self.screen_height))
        pygame.display.update()
        self.clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 100)
        text = font.render('Score:', True, self.white)
        self.canvas.blit(text, [480 * self.screen_widht / 1200, 0])
        
        for i in range(20):
            self.balls[i] = Ball(self.canvas, self.screen_widht, self.screen_height)
        self.square = Square(self.canvas, self.screen_widht, self.screen_height)
        # draws red frame
        pygame.draw.line(self.canvas, self.red, (100, 100),
                         (self.screen_widht - 100, 100), 10)
        pygame.draw.line(self.canvas, self.red,  (self.screen_widht - 100, 100),
                        (self.screen_widht - 100, self.screen_height - 100), 10)
        pygame.draw.line(self.canvas, self.red, 
                         (self.screen_widht - 100, self.screen_height - 100),
                         (100, self.screen_height - 100), 10)
        pygame.draw.line(self.canvas, self.red, (100, self.screen_height - 100),
                         (100, 100), 10)
        # initializing player
        font_start = pygame.font.SysFont(None,
                                         int(60 * self.screen_widht / 1200))
        text_start = font_start.render(
            'To start enter your nickname in console', True, self.white
            )
        self.canvas.blit(
            text_start,
            [200 * self.screen_widht / 1200, 400 * self.screen_height / 900]
            )
        pygame.display.update()
        self.nickname = input('enter your nickname ')
        pygame.draw.line(
            self.canvas, self.black,
            (int(1 * self.screen_widht / 12), int(4 * self.screen_height / 9)),
            (self.screen_widht - 100, int(4 * self.screen_height / 9)),
            int(15 * self.screen_height / 90)
            )

    def playing(self):
        pygame.display.update()
        while not self.finished:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for ball in self.balls:
                        if (ball.status):
                            x, y = event.pos
                            if(ball.shot(x, y)):
                                self.score += 1;
                    if(self.square.status):
                        x, y = event.pos
                        if(self.square.shot(x,y)):
                            self.score += 10
            # writing current score
            font = pygame.font.SysFont(None, 100)                
            text = font.render('Score:' + str(self.score), True, self.white)
            pygame.draw.line(self.canvas, self.black, (0, 0),
                             (self.screen_widht - 100, 0),
                             int(150 * self.screen_height / 900))
            self.canvas.blit(text, [480 * self.screen_widht / 1200, 0] )
            # moving targets   
            self.square.move()    
            for ball in self.balls:
                ball.move()
            # drawing red frame
            pygame.draw.line(self.canvas, self.red, (100, 100),
                             (self.screen_widht - 100, 100), 10)
            pygame.draw.line(
                self.canvas, self.red, (self.screen_widht - 100, 100),
               (self.screen_widht - 100, self.screen_height - 100), 10
               )
            pygame.draw.line(
                self.canvas, self.red,
                (self.screen_widht - 100, self.screen_height - 100),
                (100, self.screen_height - 100), 10
                )
            pygame.draw.line(self.canvas, self.red,
                             (100, self.screen_height - 100), (100, 100), 10)
            pygame.display.update()
            # adding new balls
            if(self.clock_ball > self.spawn_period_ball):
                self.flag = True
                self.flag1 = True
                for ball in self.balls:
                    if(ball.status() == False and self.flag == True):
                        ball.rebirth()
                        self.flag = False
                if(self.flag == True):
                    print('game over')
                    self.finished = True
                else:
                    self.clock_ball = 0
            # adding square
            if(self.clock_square > self.spawn_period_square):
                if(self.square.status() == False and self.flag1 == True):
                    if(self.square.status() == False and self.flag1 == True):
                        self.square.rebirth()
                        self.flag1 = False
                self.clock_square = 0
            self.clock_ball += 1
            self.clock_square += 1

    def ending(self):
        # reading score table from the file
        with open('results_table.txt', 'r') as table:
            score_list = table.readlines()
        self.flag = True
        for player_number in range(len(score_list)):
            score_list[player_number] = score_list[player_number].rstrip()
            score_list[player_number] = score_list[player_number].split(':')
        for player in score_list:
            if(player[0] == self.nickname):
                self.flag1 = 0
                self.flag = False
                if(int(player[1]) < self.score):
                    player[1] = str(self.score)
        # writing new score table in the file
        if self.flag:
           for i in range(len(score_list)):
                if(int(score_list[i][1]) < self.score and self.flag):
                    score_list.insert(i, (self.nickname, str(self.score)))
                    self.flag = False 
        with open('results_table.txt', 'w') as table:
	        for i in range(len(score_list)):
		        print(score_list[i][0] + ':' + score_list[i][1], file = table)
        pygame.quit()
    
    
