import time
import heapq
import numpy as np


class Board:
    parent = None
    state = None
    operator = None
    depth = 0
    zero = None
    cost = 0
    final = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

    # constructor which we dfine parent curr state operators depth cost and goal state
    def __init__(self, state, parent=None, operator=None, depth=0):
        self.parent = parent
        self.state = np.array(state)
        self.operator = operator
        self.depth = depth
        self.zero = self.find_0()
        self.cost = self.depth + self.manhattan()
        self.final = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])

    # less than operator for A*
    def __lt__(self, other):
        if self.cost != other.cost:
            return self.cost < other.cost
        else:
            op_pr = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
            return op_pr[self.operator] < op_pr[other.operator]

    def __str__(self):
        return str(self.state[:3]) + '\n' \
            + str(self.state[3:6]) + '\n' \
            + str(self.state[6:]) + ' ' + str(self.depth) + str(self.operator) + '\n'

    # our goal test function
    def goal_test(self):
        if np.array_equal(self.state, self.final):
            return True
        else:
            return False

    # find index of first 0
    def find_0(self):
        for i in range(9):
            if self.state[i] == 0:
                return i

    # Heuristic function for A*
    def manhattan(self):
        state = self.index(self.state)
        goal = self.index(self.final)
        return sum((abs(state // 3 - goal // 3) + abs(state % 3 - goal % 3))[1:])

    # return indicies
    @staticmethod
    def index(state):
        index = np.array(range(9))
        for x, y in enumerate(state):
            index[y] = x
        return index

    # swaping two elements
    def swap(self, i, j):
        new_state = np.array(self.state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    # move up
    def up(self):
        if self.zero > 2:
            return Board(self.swap(self.zero, self.zero - 3), self, 'Up', self.depth + 1)
        else:
            return None

    # move down
    def down(self):
        if self.zero < 6:
            return Board(self.swap(self.zero, self.zero + 3), self, 'Down', self.depth + 1)
        else:
            return None

    # move left
    def left(self):
        if self.zero % 3 != 0:
            return Board(self.swap(self.zero, self.zero - 1), self, 'Left', self.depth + 1)
        else:
            return None

    # move right
    def right(self):
        if (self.zero + 1) % 3 != 0:
            return Board(self.swap(self.zero, self.zero + 1), self, 'Right', self.depth + 1)
        else:
            return None

    # find list of neighbors
    def neighbors(self):
        neighbors = [self.up(), self.down(), self.left(), self.right()]
        return list(filter(None, neighbors))

    __repr__ = __str__


class AStar:
    solution = None
    frontier = None
    nodes_expanded = 0
    max_depth = 0
    explored_nodes = set()
    initial_state = None

    def __init__(self, initial_state):
        self.explored_nodes.clear()
        self.initial_state = initial_state
        self.frontier = []
        self.cnt_frontier = 0

    def solve(self):
        # automatically sorts by depth + manhattan(defined __lt__ in board class)
        heapq.heappush(self.frontier, self.initial_state)
        self.cnt_frontier += 1
        while self.cnt_frontier:
            # pop the best cost = depth + manhattan
            board = heapq.heappop(self.frontier)
            self.cnt_frontier -= 1
            self.explored_nodes.add(tuple(board.state))
            # goal test
            if board.goal_test():
                break
            # expand all neighbors of that node
            for neighbor in board.neighbors():
                if tuple(neighbor.state) not in self.explored_nodes:
                    heapq.heappush(self.frontier, neighbor)
                    self.cnt_frontier += 1
                    self.explored_nodes.add(tuple(neighbor.state))
                    self.max_depth = max(self.max_depth, neighbor.depth)
        return


with open('Examples.txt') as f:
    easy_lines = f.readlines()

easy = []
for line in easy_lines:
    easy.append(eval(line))

sum_run_time = 0
for i in range(0, len(easy)):
    p = Board(easy[i])
    s = AStar(p)

    t0 = time.time()
    s.solve()
    t1 = time.time()

    run_time = t1 - t0

    sum_run_time += run_time

print(sum_run_time / 55)
