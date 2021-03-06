#########################################
## Inspiration for functions courtesy of https://github.com/sezan92/ReinforcementOpenAi
#########################################
import gym
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
slow = False
env = gym.make("MountainCar-v0")
render_simulation = False
##########################
## initializing constants
position_start = env.observation_space.low[0] #  -1.2
position_end = env.observation_space.high[0]  #   0.6
speed_start = env.observation_space.low[1]    # -0.07
speed_end = env.observation_space.high[1]     #  0.07
number_of_bins = 60
learning_rate = 0.8
gamma = 0.9
number_of_episodes = 10000
reward_list = []

##############################
## discretize the environment
def discretize(start, end, bins):
    bin_width = (end - start) / bins
    return_array = [start]
    for i in range(1, bins):
        return_array.append(start + i * bin_width)
    return_array.append(end)
    return return_array

###############################
## set poisiton and speed bins
position_bins = discretize(position_start, position_end, number_of_bins)
speed_bins = discretize(speed_start, speed_end, number_of_bins)

##################################
## set position-speed state pairs
states = []
for i in position_bins:
    for j in speed_bins:
      states.append(np.array([i,j]))
states = np.array(states)

Q = np.zeros([len(states), env.action_space.n])
############################
## Prep for value to states
position = []
speed = []
for s in states:
    position.append(s[0])
    speed.append(s[1])

position = set(position)
speed = set(speed)

########################
## Prep for heatmap
pos = []
spe = []
for s in states:
    pos.append(str(s[0]))
    spe.append(str(s[1]))
pos = set(pos)
spe = set(spe)
df_heatmap = pd.DataFrame(index = pos, columns = spe)
df_heatmap.index = df_heatmap.index.map(float)
df_heatmap.columns = df_heatmap.columns.map(float)
df_heatmap = df_heatmap.sort_index(axis = 0)
df_heatmap = df_heatmap.sort_index(axis = 1)
df_heatmap.index = df_heatmap.index.map(str)
df_heatmap.columns = df_heatmap.columns.map(str)
df_heatmap = df_heatmap.fillna(0)

##############################################
## x represents the observed (position,speed)
def map_observation_to_state(x, states, pos, speed):
    closest_position = min(position, key = lambda y:abs(y - x[0]))
    closest_speed = min(speed, key = lambda y:abs(y - x[1]))
    n = np.array((closest_position,closest_speed))
    state_index = np.where((states == n).all(axis = 1))[0][0]
    return state_index

##############
## Q-learning
for i in range(number_of_episodes):
    initial_state = env.reset()
    if render_simulation == True:
        env.render()
    state = map_observation_to_state(initial_state, states, position, speed)
    all_rewards = 0
    done = False
    j = 0
    while j < 200:
        j += 1
        action = np.argmax(Q[state,:])
        observation, reward, done, _ = env.step(action)
        next_state = map_observation_to_state(observation, states, position, speed)
        if render_simulation == True:
            env.render()
        Q[state,action] += learning_rate * (reward + gamma * np.max(Q[next_state,:]) - Q[state,action])

        state_pos = str(states[state][0])
        state_speed = str(states[state][1])
        df_heatmap[str(state_speed)][str(state_pos)] = np.argmax(Q[state,:])
        all_rewards += reward
        state = next_state
        if j == 199 or done == True:
            if done == False:
                print ("FAILED")
            else:
                print("SUCCEEDED")
            print ("Episode " + str(i) + ": Reward: " + str(all_rewards))
            reward_list.append(all_rewards)
            break


df_heatmap = df_heatmap.fillna(0)

df_heatmap.to_csv('./heatmap2.csv', index = False)

plt.ion()
sns.heatmap(df_heatmap)
plt.show()
