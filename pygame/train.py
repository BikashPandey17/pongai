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

SIZE = 10

HM_EPISODES = 3000
MOVE_PENALTY = 0
ENEMY_PENALTY = 300
BOUNCE_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9998  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 100  # how often to play through env visually.

start_q_table = None # None or Filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95



if start_q_table is None:
    # initialize the q-table#
    q_table = {}
    for i in range(0, 20): # x axis is divided in 14 parts
        for ii in range(-9, 10): # y axis is divided in 10 parts
            for iii in range(-8, 9): # for x velocity
                    for iiii in range(-8, 9): # for y velocity
                        q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(2)] # only two actions 0(UP) and 1(DOWN)
else:
    with open(start_q_table, "rb") as f:
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

for episode in range(HM_EPISODES):
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

    # if episode % SHOW_EVERY == 0:
    print(f"on #{episode}, epsilon is {epsilon}")
    print(f"{episode} ep reward_mean: {np.mean(episode_rewards[-episode:])}")
    #     show = True
    # else:
    #     show = False
    episode_reward = 0
    # -------- Main Program Loop -----------
    while carryOn:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop

        obs = get_obs(paddleB, ball)
        #print(obs)
        if np.random.random() > epsilon:
            # GET THE ACTION
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 2)

        # Take the action!
        paddleB.action(action)
        
        # --- Game logic should go here
        all_sprites_list.update()

        reward = -MOVE_PENALTY
        #Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x>670:
            reward = -ENEMY_PENALTY # paddle ne hug diya 
        if ball.rect.x<=0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y>490:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y<0:
            ball.velocity[1] = -ball.velocity[1]

        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddleB):
            reward = BOUNCE_REWARD
            ball.bounce()

        # --- Drawing code should go here
        # First, clear the screen to black. 
        screen.fill(BLACK)
        
        
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # --- Limit to 60 frames per second
        clock.tick(1000)

        ## NOW WE KNOW THE REWARD, LET'S CALC YO
        # first we need to obs immediately after the move.
        new_obs = get_obs(paddleB, ball)
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[obs][action] = new_q

        episode_reward += reward
        if reward == -ENEMY_PENALTY:
            carryOn = False
    
    #print(episode_reward)
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY
    #Once we have exited the main program loop we can stop the game engine:
    pygame.quit()


    moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.plot(f'plot--{int(time.time())}.png')

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)