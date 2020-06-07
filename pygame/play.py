# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

with open("qtable-1591556415.pickle", "rb") as f:
    q_table = pickle.load(f)

def get_obs(paddle, ball):
    # to return the normalized observation
    x_range = 700/20
    y_range = 500/10
    
    paddle_x = np.floor((paddle.rect.x)/x_range) + 35
    paddle_y = np.floor((paddle.rect.y)/y_range) + 50

    ball_x = np.floor((ball.rect.x)/x_range) + 35
    ball_y = np.floor((ball.rect.y)/y_range) + 50


    return ((paddle_x-ball_x,paddle_y-ball_y),(ball.velocity[0], ball.velocity[1]))


# can look up from Q-table with: print(q_table[((-9, -2), (3, 9))]) for example

episode_rewards = []


pygame.init()

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

# we need to create and position our sprites

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE,10,10)
ball.rect.x = 10
ball.rect.y = 195

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the paddles to the list of sprites

all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop

    obs = get_obs(paddleB, ball)
    #print(obs)
    action = np.argmax(q_table[obs])

    # Take the action!
    paddleB.action(action)
    
    # --- Game logic should go here
    all_sprites_list.update()

    #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>670:
        ball.velocity[0] = -ball.velocity[0] # paddle ne hug diya 
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]

    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    # --- Drawing code should go here
    # First, clear the screen to black. 
    screen.fill(BLACK)
    
    
    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(60)

   
pygame.quit()
