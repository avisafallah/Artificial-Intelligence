import numpy as np
import pandas as pd


# Class defined to create our test environment
# Purpose: To define the structure of the environment and actions possible
# To get / set the status of the environment based on the Agent's movement
class ENV:
    def __init__(self):
        self.blocks = [(0, 1), (1, 5), (2, 5), (3, 0), (3, 1), (3, 3), (3, 4), (3, 6),
                       (4, 2), (4, 4), (4, 6), (4, 7), (4, 8), (5, 2), (5, 4), (7, 6),
                       (7, 7), (7, 8), (7, 9), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
                       (9, 7)]
        self.flags = [(2, 0), (1, 3), (2, 6), (4, 5), (7, 1), (4, 1), (9, 8)]
        self._flags = [(2, 0), (1, 3), (2, 6), (4, 5), (7, 1), (4, 1), (9, 8), (9, 9)]
        self.flags_default = [(2, 0), (1, 3), (2, 6), (4, 5), (7, 1), (4, 1), (9, 8)]



        # dont uncomment until poping
        # self._flags = [(2, 0), (1, 3), (2, 6), (4, 5), (7, 1), (4, 1), (8, 0), (9, 8)]
        self.captured_flags = []
        self.cnt_flags = len(self.flags)
        self.state_row_cnt = 10
        self.state_col_cnt = 10
        self.agent_path = []
        self.action_cnt = 4
        self.actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']  # four possible actions in this environment

        self.states = np.full((self.state_row_cnt, self.state_col_cnt), '-')  # individual states represented as - in the environment
        self.goal_state = (9, 9)
        self.states[0][0] = 'A'  # Agent
        for block in self.blocks:   # Blocks
            self.states[block[0]][block[1]] = 'B'
        self.flags_string = ""
        for flag in self.flags:
            self.flags_string += '0'
            self.states[flag[0]][flag[1]] = 'F'
        # self.states[1][2] = '|'  # holes
        # self.states[2][3] = '|'
        # self.states[3][0] = '|'
        self.states[self.goal_state[0]][self.goal_state[1]] = 'G'  # Goal or destination to reach
        # Agent's init position at [0,0]
        self.A_in_row = 0
        self.A_in_col = 0

    # used for getting current flags captured
    def getFlagStr(self):
        return self.flags_string

    # used while creating a Q class to know what all possible actions are offered by this environment
    def getActionItems(self):
        return self.action_cnt, self.actions

    # used mainly to test the agent that was learnt already
    def getAgentPosition(self):
        return self.A_in_row, self.A_in_col

    def is_illusion(self, action):
        if action == 'UP':
            if (self.A_in_row - 1, self.A_in_col) in self.captured_flags:
                return True
        if action == 'DOWN':
            if (self.A_in_row + 1, self.A_in_col) in self.captured_flags:
                return True
        if action == 'LEFT':
            if (self.A_in_row, self.A_in_col - 1) in self.captured_flags:
                return True
        if action == 'RIGHT':
            if (self.A_in_row, self.A_in_col) in self.captured_flags:
                return True


    def nearest_flag(self, stateR, stateC):
        min_dist = pow((pow((self._flags[0][0] - stateR), 2) + pow((self._flags[0][1] - stateC), 2)), 0.5)
        return (14 - min_dist) / 10

    def duplicate_path(self, stateR, stateC):
        counter = 0
        for pos in self.agent_path:
            if stateR == pos[0] and stateC == pos[1]:
                counter += 1

        return max(-counter * 0.2, -1)

    # to check if the agent has reached the destination or fell into any of the three holes in the environment
    def is_sth(self, stateR, stateC):
        done = False
        if (stateR, stateC) in self.blocks or (stateR, stateC) == self.goal_state or (stateR, stateC) in self.flags:
            done = True

        return done

    # used for display purpose
    def render(self):
        return (
        "{}\n".format(pd.DataFrame(self.states).to_string(index=False, header=False)), (self.A_in_row, self.A_in_col))

        # function: step taken by the agent. One of the four actions would be input to this function.

    # Function would update the environment's state based on the input action and returns the next state,the reward received by the agent and
    # status info if the Agent has reached the destination/ fallen in the hole ('done' variable = true)
    def step(self, action):
        done = False
        prev_A_in_row = self.A_in_row
        prev_A_in_col = self.A_in_col

        if action == 'UP':
            self.A_in_row = self.A_in_row - 1
            if self.A_in_row < 0:
                R = -100
                next_state = (self.A_in_row+1, self.A_in_col)
                self.A_in_row = prev_A_in_row
                self.A_in_col = prev_A_in_col
                print('out of range')
                return next_state, R, done, self.flags_string

        if action == 'DOWN':
            self.A_in_row = self.A_in_row + 1
            if self.A_in_row == self.state_row_cnt:
                R = -100
                next_state = (self.A_in_row-1, self.A_in_col)
                self.A_in_row = prev_A_in_row
                self.A_in_col = prev_A_in_col
                print('out of range')
                return next_state, R, done, self.flags_string

        if action == 'LEFT':
            self.A_in_col = self.A_in_col - 1
            if self.A_in_col < 0:
                R = -100
                next_state = (self.A_in_row, self.A_in_col+1)
                self.A_in_row = prev_A_in_row
                self.A_in_col = prev_A_in_col
                print('out of range')
                return next_state, R, done, self.flags_string

        if action == 'RIGHT':
            self.A_in_col = self.A_in_col + 1
            if self.A_in_col == self.state_col_cnt:
                R = -100
                next_state = (self.A_in_row, self.A_in_col-1)
                self.A_in_row = prev_A_in_row
                self.A_in_col = prev_A_in_col
                print('out of range')
                return next_state, R, done, self.flags_string

        penalty_duplicate = self.duplicate_path(self.A_in_row, self.A_in_col)
        # penalty_duplicate = 0
        self.agent_path.append((self.A_in_row, self.A_in_col))
        if not self.is_sth(self.A_in_row, self.A_in_col):
            self.states[prev_A_in_row][prev_A_in_col] = '-'
            self.states[self.A_in_row][self.A_in_col] = 'A'

            next_state = (self.A_in_row, self.A_in_col)
            # R = -0.1 + self.nearest_flag(self.A_in_row, self.A_in_col) +
            # penalty_duplicate(self.A_in_row, self.A_in_col)
            R = -0.1

            return next_state, R, done, self.flags_string


        else:
            if (self.A_in_row, self.A_in_col) == self.goal_state:  # Target reached. Add reward = 1
                done = True
                self.states[prev_A_in_row][prev_A_in_col] = '-'
                self.states[self.A_in_row][self.A_in_col] = 'A'
                print('Target reached')
                R = 100.0 - len(self.flags) / self.cnt_flags

                next_state = (self.A_in_row, self.A_in_col)
                return next_state, R, done, self.flags_string

            elif (self.A_in_row, self.A_in_col) in self.flags:
                self.states[prev_A_in_row][prev_A_in_col] = '-'
                self.states[self.A_in_row][self.A_in_col] = 'A'

                index = self.flags_default.index((self.A_in_row, self.A_in_col))
                self.flags_string = self.flags_string[:index] + '1' + self.flags_string[index + 1:]
                self.captured_flags.append((self.A_in_row, self.A_in_col))
                self.flags.remove((self.A_in_row, self.A_in_col))
                self._flags.remove((self.A_in_row, self.A_in_col))
                print('Flag Captured')
                R = 10

                next_state = (self.A_in_row, self.A_in_col)
                return next_state, R, done, self.flags_string
            else:
                R = -100
                next_state = (prev_A_in_row, prev_A_in_col)
                self.A_in_row = prev_A_in_row
                self.A_in_col = prev_A_in_col
                print('blocked')
                return next_state, R, done, self.flags_string

