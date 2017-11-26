
import gym
import numpy as np

slow = True
env = gym.make("MountainCar-v0")

position_start = env.observation_space.low[0]
position_end = env.observation_space.high[0]
speed_start = env.observation_space.low[1]
speed_end = env.observation_space.high[1]
number_of_bins = 20


def discretize(start, end, bins):
    bin_width = (end - start) / bins
    return_array = [start]
    for i in range(1, bins):
        return_array.append(start + i*bin_width)
    return_array.append(end)
    return return_array

position_bins = discretize(position_start, position_end, number_of_bins)
speed_bins = discretize(speed_start, speed_end, number_of_bins)
states = []
for i in position_bins:
    for j in speed_bins:
      states.append(np.array([i,j]))
states = np.array(states)

################
## Prep for value to states
pos = []
speed = []
for s in states:
    pos.append(s[0])
    speed.append(s[1])


######################
## x represents the observed (position,speed)
def map_observation_to_state(x, states, pos, speed):

    closest_position = min(pos, key=lambda y:abs(y-x[0]))
    closest_speed = min(speed, key=lambda y:abs(y-x[0]))
    n = np.array((closest_position,closest_speed))
    state_index = np.where((states==n).all(axis=1))[0][0]
    return state_index














print(position_bins)
print(speed_bins)
