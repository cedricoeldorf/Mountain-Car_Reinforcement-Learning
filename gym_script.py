
import gym
import numpy as np
slow = True
env = gym.make("MountainCar-v0")

#############
# Calculate maximum/minimum position and speed for discretization
#############
max_position = env.observation_space.high[0]
min_position = env.observation_space.low[0]
max_speed = env.observation_space.high[1]
min_speed = env.observation_space.low[1]

NUM_BUCKETS = (10, 10, 14, 14)
NUM_ACTIONS = env.action_space.n
ACTION_INDEX = len(NUM_BUCKETS)

###########
## table to fill in
############
q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,))

for _ in range(0,10):
    observation = env.reset()
    done = False
    timesteps = 0
    while not done:
        if slow: env.render()

        # Decide on an action
        action = env.action_space.sample() # your agent here (this takes random actions)

        # take action
        observation, reward, done, info = env.step(action)
        timesteps+=1

        if slow: print(observation)
        if slow: print(reward)
        if slow: print(done)
    print("Episode finished after ", timesteps, "timesteps.")


# what we need to do? (maybe?)
#

## value iteration
# - evaluate rewards and transitions
# - Create Q
# - update policy
