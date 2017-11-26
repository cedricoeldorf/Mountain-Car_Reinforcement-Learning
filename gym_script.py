
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

def value_to_state(x, states):
    pos = []
    speed = []
    for s in states:
        


    closest_position = min(states, key=lambda x:abs(x-myNumber))xpos=np.digitize(x[0],pos_bins)
    xvel=np.digitize(x[1],vel_bins)
    stateValue = np.array([pos_bins[xpos],vel_bins[xvel]])
    state = np.where((allStates==stateValue).all(axis=1))[0][0]
    return state

def find_in_states (x, states):
    for i in states[0]












print(position_bins)
print(speed_bins)
