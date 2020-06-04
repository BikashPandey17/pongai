import gym 
import numpy as np
from matplotlib import pyplot as plt 

# Create the environment 
env = gym.make("MountainCar-v0")


# Learning rate without decay 
LEARNING_RATE = 0.1
# Is a measure of how important are our future actions over current actions
DISCOUNT = 0.95 
# Total episodes for an agent to learn
EPISODES = 1000

SHOW_EVERY = 100

# Higher the EPSILON, more likely we are to perform a random action 
EPSILON = 0.5
START_EPSILON_DECAYING = 1
# Integer Divison 
END_EPSILON_DECAYING = EPISODES // 2
EPSILON_DECAY_VALUE = EPSILON / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

# Building the Q-Table
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
# Separate the range into 20 discrete buckets 
DISCRETE_OS_WIN_SIZE = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

# Initializing the Q-table
# 20 * 20 * 3 table that contains combination of all possible position and velocity 
# First it stores random values in the range of 0 - (-2) but over time it slowliy gets optimized and we choose the maximum value for each action to get a poitive reward 
q_table = np.random.uniform(low = -2, high = 0, size = (DISCRETE_OS_SIZE + [env.action_space.n]))
# List keeping track of the episode reward 
episode_rewards = [] 
# Dictionary 
aggregate_episode_rewards = {'epi' : [], 'avg' : [], "min" : [], 'max' : []}


# Create a discrete value for all the continuous state values thar are returned 
def get_discrete_state(state):
	DISCRETE_STATE = (state - env.observation_space.low) / DISCRETE_OS_WIN_SIZE
	return tuple(DISCRETE_STATE.astype(np.int))

for episode in range(EPISODES): 
	episode_reward = 0
	if episode % SHOW_EVERY == 0: 
		print(episode)
		render = True
	else: 
		render = False 

	DISCRETE_STATE = get_discrete_state(env.reset())
	done = False

	while not done: 
		# Step t hrough the environment
		# There are 3 actions for this particular environment
		# 0 - push left, 1 - do nothing, 2 - push right
		if np.random.random() > EPSILON:
			action = np.argmax(q_table[DISCRETE_STATE])
		else:
			action = np.random.randint(0, env.action_space.n)
		# Every time we perform an action we will get a new state, a reward, and check if the game is done 
		new_state, reward, done, _ = env.step(action)
		episode_reward += reward
		new_discrete_state = get_discrete_state(new_state)
		# Reward will be -1 until we reach the flag, where the reward becomes zero 
		if render: 
			env.render()
		if not done: 
			max_future_q = np.max(q_table[new_discrete_state])
			current_q = q_table[DISCRETE_STATE + (action, )]
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
			q_table[DISCRETE_STATE + (action, )] = new_q

		# Set a reward 0 when the goal is achieved 
		elif new_state[0] >= env.goal_position: 
			# print(f"We made it on episode {episode}")
			q_table[DISCRETE_STATE + (action, )] = 0 

		DISCRETE_STATE = new_discrete_state

	if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
		EPSILON -= EPSILON_DECAY_VALUE

	# Append the total reward calculated after each episode 
	episode_rewards.append(episode_reward)

	if not episode % SHOW_EVERY: 
		average_reward = sum(episode_rewards[-SHOW_EVERY:]) / len(episode_rewards[-SHOW_EVERY:])
		aggregate_episode_rewards['epi'].append(episode)
		aggregate_episode_rewards['avg'].append(average_reward)
		aggregate_episode_rewards['min'].append(min(episode_rewards[-SHOW_EVERY:]))
		aggregate_episode_rewards['max'].append(max(episode_rewards[-SHOW_EVERY:]))

		print(f"Episode : {episode} avg : {average_reward} min : {min(episode_rewards[-SHOW_EVERY:])} max : {max(episode_rewards[-SHOW_EVERY:])}" )
# When all done 
env.close()

plt.plot(aggregate_episode_rewards['epi'], aggregate_episode_rewards['avg'], label = "avg")
plt.plot(aggregate_episode_rewards['epi'], aggregate_episode_rewards['min'], label = "min")
plt.plot(aggregate_episode_rewards['epi'], aggregate_episode_rewards['max'], label = "max")
plt.legend(loc = 'upper right')
plt.show()