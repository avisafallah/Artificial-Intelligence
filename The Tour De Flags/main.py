import env
import numpy as np
import pandas as pd
from tkinter import *
import json
import time
def saver(dictex):
    for key, val in dictex.items():
        val.to_csv("data_{}.csv".format(str(key)))
    with open("keys.txt", "w") as f: #saving keys to file
        f.write(str(list(dictex.keys())))

def loader():
    """Reading data from keys"""
    with open("keys.txt", "r") as f:
        keys = eval(f.read())
    dictex = {}
    for key in keys:
        dictex[key] = pd.read_csv("data_{}.csv".format(str(key)))
    return dictex

##update Agent's current position info as text field and the environment's state changes in the display
def display_environment(env1):
    global txt, pos, wdw
    txt1, txt2 = env1.render()

    txt.delete("1.0", "end")
    txt.insert(END, txt1)

    wdw.update()
    # time.sleep(0.25)

def display_environment_test(env1):
    global txt, pos, wdw
    txt1, txt2 = env1.render()

    txt.delete("1.0", "end")
    txt.insert(END, txt1)

    pos.set("Agent's position : " + str(txt2))
    wdw.update()
    time.sleep(0.25)

# Main class that creates Q table, implements bellmans equation to update the Q table based on the
# Agent's action. Agent learning happens here.
class Q:
    # Q table creation
    def __init__(self, gamma=0.9, alpha=0.1, epsilon=0.1, num_episodes=100):
        self.q_tables = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_episodes = num_episodes
        self.env1 = env.ENV()
        self.action_count, self.actions = self.env1.getActionItems()

    def get_q_tables(self):
        return self.q_tables
    # reseting environment is easier with this OO approach. Just create a new environment object
    # and returns the agents position as (0,0).
    def reset_environment(self):
        del self.env1
        self.env1 = env.ENV()
        return self.env1.getAgentPosition()

    # main learning algorithm. loops for 'number of episodes'
    # on a new environment created per episode, agent tries to make many movements (one of the four actions possible)
    # either randomly or based on the Q values determined during the update process.
    def learn(self):
        for episode_cnt in range(self.num_episodes):
            print('episode: {}'.format(episode_cnt), end='\t')
            state = self.reset_environment()
            display_environment(self.env1)
            done = self.env1.is_sth(state[0], state[1])
            flags_str = self.env1.getFlagStr()

            if flags_str not in self.q_tables:
                q_table = pd.DataFrame(0, index=pd.MultiIndex.from_product(
                    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]),
                                       columns=['UP', 'DOWN', 'LEFT', 'RIGHT'])
                self.q_tables[flags_str] = q_table
            while not done:
                # give 10% chance to choose an action randomly and also in a state where
                # all actions have Q values == 0 (init state), choose action randomly
                if (np.random.uniform() < self.epsilon) or ((self.q_tables[flags_str].loc[state, :] == 0).all()):
                    action = np.random.choice(self.actions)
                # 90% of the chance it picks up the action corresponding to the max Q value
                else:
                    action = self.q_tables[flags_str].loc[state, :].index[self.q_tables[flags_str].loc[state, :].values.argmax()]
                    while self.env1.is_illusion(action):
                        print("illusion")
                        action = np.random.choice(self.actions)

                next_state, Reward, done, flags_str_new = self.env1.step(action)
                # print("!!!!!!!!!", Reward)

                current_Q = self.q_tables[flags_str].loc[state, action]
                next_Q = self.q_tables[flags_str].loc[next_state, :].max()

                # bellman's equations and its discounted rewards in future
                self.q_tables[flags_str].loc[state, action] += self.alpha * (Reward + self.gamma * next_Q - current_Q)
                if Reward == -100:
                    self.q_tables[flags_str].loc[state, action] = Reward

                if flags_str != flags_str_new and flags_str_new not in self.q_tables:
                    q_table_new = pd.DataFrame(0, index=pd.MultiIndex.from_product(
                        [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]),
                                           columns=['UP', 'DOWN', 'LEFT', 'RIGHT'])
                    flags_str = flags_str_new
                    self.q_tables[flags_str] = q_table_new

                flags_str = flags_str_new
                state = next_state
                display_environment(self.env1)

            saver(self.q_tables)


txt = None
pos = None
wdw = None


# Interface class for test_env.py for training init on a button press
class Q_train:
    def __init__(self, wdw1, text_box1, position_info):
        global wdw, txt, pos

        wdw = wdw1
        txt = text_box1
        pos = position_info

    def train(self):
        q = Q(gamma=0.9, alpha=0.1, epsilon=0.2, num_episodes=100)
        q.learn()
        return q.get_q_tables()


##Interface class for test_env.py for testing the agent on a button press
class Q_test:
    def __init__(self, wdw1, text_box1, position_info):
        global wdw, txt, pos

        wdw = wdw1
        txt = text_box1
        pos = position_info
        self.q_table = {}
        self.final_episode = {}

    def test(self, qt):

        try:
            self.q_table = qt
        except:
            txt.delete("1.0", "end")
            txt.insert(END, 'Try to train the Agent before testing it\n')
            return

        if self.q_table is not None:
            env1 = env.ENV()
            display_environment_test(env1)  # display the init state of the environment
            done = False
            while not done:  # until it reaches the destination
                state = env1.getAgentPosition()  # get current position
                flags_str = env1.getFlagStr()
                state_str = str(state[0])
                state_str += "," + str(state[1])
                self.final_episode[state_str] = self.q_table[flags_str].loc[state, :]
                print(self.q_table[flags_str].loc[state, :])
                action = self.q_table[flags_str].loc[state, :].index[self.q_table[flags_str].loc[state, :].values.argmax()]  # fetch the next best possible action from the Q table learnt
                a, b, done, c = env1.step(action)  # execute the action
                display_environment_test(env1)  # display the update

