import gym
import numpy as np
slow = False
env = gym.make("MountainCar-v0")

position_start = env.observation_space.low[0]
position_end = env.observation_space.high[0]
speed_start = env.observation_space.low[1]
speed_end = env.observation_space.high[1]
number_of_bins = 99

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
pos = set(pos)
speed = set(speed)
######################
## x represents the observed (position,speed)
def map_observation_to_state(x, states, pos, speed):

    closest_position = min(pos, key=lambda y:abs(y-x[0]))
    closest_speed = min(speed, key=lambda y:abs(y-x[1]))
    n = np.array((closest_position,closest_speed))
    state_index = np.where((states==n).all(axis=1))[0][0]
    return state_index




Q = np.zeros([len(states), env.action_space.n])
learning_rate = 0.8
gamma = 0.9
number_of_episodes= 30000
reward_list = []

for i in range(number_of_episodes):
    initial_state = env.reset()
    state = map_observation_to_state(initial_state, states, pos, speed)
    all_rewards =0
    done = False
    j = 0
    while j<200:
        j+=1

        # #############################################################################
        action = np.argmax(Q[state,:]+np.random.randn(1,env.action_space.n)*(1./(i+1)))
        # #############################################################################

        observation, reward, done, _ = env.step(action)
        next_state = map_observation_to_state(observation, states, pos, speed)
        #env.render()
        Q[state,action] += learning_rate*(reward+gamma*np.max(Q[next_state,:])-Q[state,action])
        all_rewards += reward
        state = next_state
        if done ==True or j==199:
            if done == False:
                print ("FAILED")
            else:
                print("SUCCEEDED")
            print ("Episode " + str(i) + ": Reward: " + str(all_rewards))
            #print ("================================================")
            #print(Q)
            #print ("================================================")
            reward_list.append(all_rewards)
            break
