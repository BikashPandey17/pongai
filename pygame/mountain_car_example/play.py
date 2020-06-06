import gym
import numpy as np

env = gym.make("MountainCar-v0")
state = env.reset()

q_table = np.load("qtables/900-qtable.npy")
EPISODES = 10
# Building the Q-Table
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
# Separate the range into 20 discrete buckets 
DISCRETE_OS_WIN_SIZE = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

# Create a discrete value for all the continuous state values thar are returned 
def get_discrete_state(state):
	DISCRETE_STATE = (state - env.observation_space.low) / DISCRETE_OS_WIN_SIZE
	return tuple(DISCRETE_STATE.astype(np.int))

for episode in range(EPISODES):
    discrete_state = get_discrete_state(env.reset())
    done = False

    render = True
    print(episode)

    while not done:

        action = np.argmax(q_table[discrete_state])
        
        new_state, reward, done, _ = env.step(action)

        new_discrete_state = get_discrete_state(new_state)

        env.render()

        discrete_state = new_discrete_state


env.close()