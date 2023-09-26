import numpy as np
import random
import time
import math
import os

# MCTS move computation time
PROCESS_TIME = 3

class GameBoard:
    # Class initialization
    def __init__(self, cpu, row, col):
        self.row = row
        self.col = col
        self.turn = random.randint(1, 2)
        self.board = np.zeros(shape=(row, col))
        self.cpu = cpu

    # Print out game board on console
    def show(self):
        os.system('cls')

        print("+---", end="")
        for i in range(self.col - 1):
            print("----", end="")
        print("+")
        for j in range(self.row - 1, -1, -1):
            for i in range(self.col):
                if self.board[j, i] == 1:
                    print("| X", end=" ")
                elif self.board[j, i] == 2:
                    print("| O", end=" ")
                else:
                    print("|  ", end=" ")
            print("|")
        print("+---", end="")
        for i in range(self.col - 1):
            print("----", end="")
        print("+")
        print("| 1 ", end="")
        for i in range(self.col - 1):
            print("  {} ".format(i + 2), end="")
        print("|")

        if self.turn == self.cpu:
            print("Opponent's turn [X]")
            print("Please wait...")
        else:
            print("Your turn [O]")
            print("Enter a number between 1 and {}: ".format(self.col), end="")

    # Takes user input and play move
    def play(self):
        try:
            move = int(input())
            if move in range(1, self.col + 1):
                for i in range(6):
                    if self.board[i, move - 1] == 0:
                        self.board[i, move - 1] = self.turn
                        self.switch_turn()
                        return True
            return False
        except:
            return False

    # Check whether match is over
    def check_win(self):
        # check rows
        for y in range(self.row):
            row = list(self.board[y, :])
            for x in range(4):
                if row[x:x + 4].count(row[x]) == 4:  # out range
                    if row[x] != 0:
                        return row[x]
        # check columns
        for x in range(self.col):
            col = list(self.board[:, x])
            for y in range(4):
                if col[y:y + 4].count(col[y]) == 4:  # out range
                    if col[y] != 0:
                        return col[y]

        points = []
        for i in range(self.row):
            for j in range(self.col):
                if i - 3 >= 0 and j + 3 < self.col:
                    points.append((i, j))
        # check right diagonals

        for point in points:
            diag = list()
            for k in range(4):
                diag.append(self.board[point[0] - k, point[1] + k])
            if diag.count(1) == 4 or diag.count(2) == 4:
                return diag[0]
        # check left diagonals
        points = []
        for i in range(self.row):
            for j in range(self.col):
                if i - 3 >= 0 and j - 3 >= 0:
                    points.append((i, j))
        for point in points:
            diag = list()
            for k in range(4):
                diag.append(self.board[point[0] - k, point[1] - k])
            if diag.count(1) == 4 or diag.count(2) == 4:
                return diag[0]
        # no winner
        return None

    # Given a column, applies a move
    def apply_move(self, column):
        for i in range(self.row):
            if self.board[i, column - 1] == 0:
                self.board[i, column - 1] = self.turn
                self.switch_turn()
                return True
        return False

    # Change player turn
    def switch_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1


MAX_DEPTH = 5
PRUNING = False
class ConnectSin:
    YOU = 1
    CPU = 2
    EMPTY = 0
    DRAW = 0
    MOVE = 0
    __CONNECT_NUMBER = 4
    NODES_SEEN = 0
    board = None
    score_board = [5, 55, 555]

   # The main class for the connect4 game
   # Inputs
   # ----------
   # board_size : a tuple representing the board size in format: (rows, columns)
   # silent     : whether the game prints outputs or not
    def __init__(self, board_size=(6, 7), board=None, silent=True):

        assert len(board_size) == 2, "board size should be a 1*2 tuple"
        assert board_size[0] > 4 and board_size[1] > 4, "board size should be at least 5*5"

        self.columns = board_size[1]
        self.rows = board_size[0]
        self.silent = silent
        self.board_size = self.rows * self.columns
        self.board = board

    def __drop_piece_in_column(self, move):
        last_empty_space = 0
        column_index = move - 1
        for i in range(self.rows):
            if self.board[i][column_index] == 0:
                print(i, column_index)
                return i, column_index

    #
    # gets your input
    #
    # Output
    # ----------
    # (int) an integer between 1 and column count. the column to put a piece in
    def get_your_input(self):

        score, move = self.minimax(0, True, float("-inf"), float("inf"), use_pruning=PRUNING)
        return self.__drop_piece_in_column(move)

    def minimax(self, depth, maximizing, a, b, prev_move=0, use_pruning=True):
        self.NODES_SEEN += 1
        available_moves = self.get_possible_moves()
        if depth == MAX_DEPTH or len(available_moves) == 0 or self.check_for_winners() != 0:
            return self.heuristic(), prev_move
        best_score = float("-inf") if maximizing else float("inf")
        if use_pruning:
            random.shuffle(available_moves)
        best_move = available_moves[0]
        for move in available_moves:
            last_empty_space = 0
            column_index = move - 1
            for i in range(self.rows):
                if self.board[i][column_index] == 0:
                    last_empty_space = i
                    break

            self.board[last_empty_space][column_index] = self.YOU if maximizing else self.CPU
            next_score, ignore = self.minimax(depth + 1, not maximizing, a, b, move, use_pruning)
            self.board[last_empty_space][column_index] = self.EMPTY
            if maximizing and next_score > best_score:
                best_score = next_score
                best_move = move
                a = max(a, best_score)
                if b <= a and use_pruning:
                    break
            elif (not maximizing) and next_score < best_score:
                best_score = next_score
                best_move = move
                b = min(b, best_score)
                if b <= a and use_pruning:
                    break

        return best_score, best_move

    def heuristic(self):
        user_score = 0
        cpu_score = 0
        winner = self.check_for_winners()
        if winner == self.YOU:
            return float("inf")
        elif winner == self.CPU:
            return float("-inf")

        for k in range(2, self.__CONNECT_NUMBER):
            for i in range(self.rows):
                for j in range(self.columns - k + 1):
                    player = self.board[i][j]
                    if player == self.EMPTY:
                        continue
                    continues = True
                    for z in range(k):
                        if self.board[i][j + z] != player:
                            continues = False
                            break
                    if continues:
                        if player == self.YOU:
                            user_score += self.score_board[k - 2]
                        else:
                            cpu_score += self.score_board[k - 2]

        for k in range(2, self.__CONNECT_NUMBER):
            for i in range(self.rows - k + 1):
                for j in range(self.columns):
                    player = self.board[i][j]
                    if player == self.EMPTY:
                        continue
                    continues = True
                    for z in range(k):
                        if self.board[i + z][j] != player:
                            continues = False
                            break
                    if continues:
                        if player == self.YOU:
                            user_score += self.score_board[k - 2]
                        else:
                            cpu_score += self.score_board[k - 2]

        for k in range(2, self.__CONNECT_NUMBER):
            for i in range(self.rows - k + 1):
                for j in range(self.columns - k + 1):
                    player = self.board[i][j]
                    if player == self.EMPTY:
                        continue
                    continues = True
                    for z in range(k):
                        if self.board[i + z][j + z] != player:
                            continues = False
                            break
                    if continues:
                        if player == self.YOU:
                            user_score += self.score_board[k - 2]
                        else:
                            cpu_score += self.score_board[k - 2]

        for k in range(2, self.__CONNECT_NUMBER):
            for i in range(self.rows - k + 1):
                for j in range(self.columns - k + 1):
                    player = self.board[i + k - 1][j]
                    if player == self.EMPTY:
                        continue
                    continues = True
                    for z in range(k):
                        if self.board[i + k - 1 - z][j + z] != player:
                            continues = False
                            break
                    if continues:
                        if player == self.YOU:
                            user_score += self.score_board[k - 2]
                        else:
                            cpu_score += self.score_board[k - 2]

        return user_score - cpu_score

    #
    # checks if anyone has won in this position
    #
    # Output
    # ----------
    # (int) either 1,0,-1. 1 meaning you have won, -1 meaning the player has won and 0 means that nothing has happened

    def check_for_winners(self):
        have_you_won = self.check_if_player_has_won(self.YOU)
        if have_you_won:
            return self.YOU
        has_cpu_won = self.check_if_player_has_won(self.CPU)
        if has_cpu_won:
            return self.CPU
        return self.EMPTY

    #
    # checks if player with player_id has won
    #
    # Inputs
    # ----------
    # player_id : the id for the player to check
    #
    # Output
    # ----------
    # (boolean) true if the player has won in this position

    def check_if_player_has_won(self, player_id):
        return (
                self.__has_player_won_diagonally(player_id)
                or self.__has_player_won_horizentally(player_id)
                or self.__has_player_won_vertically(player_id)
        )

    #
    # checks if this move can be played
    #
    # Inputs
    # ----------
    # move : the column to place a piece in, in range [1, column count]
    #
    # Output
    # ----------
    # (boolean) true if the move can be played

    def is_move_valid(self, move):
        if move < 1 or move > self.columns:
            return False
        column_index = move - 1
        return self.board[self.rows - 1][column_index] == 0

    #
    # returns a list of possible moves for the next move
    #
    # Output
    # ----------
    # (list) a list of numbers of columns that a piece can be placed in

    def get_possible_moves(self):
        possible_moves = []
        for i in range(self.columns):
            move = i + 1
            if self.is_move_valid(move):
                possible_moves.append(move)
        return possible_moves

    def __has_player_won_horizentally(self, player_id):
        for i in range(self.rows):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_vertically(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_diagonally(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + self.__CONNECT_NUMBER - 1 - x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False




class MCTS:
    # Class initialization
    def __init__(self, symbol, t):
        self.symbol = symbol
        self.t = t

    # Main function for MCTS move computation
    def compute_move(self, root):
        time0 = time.time()
        while (time.time() - time0) < self.t:
            # selection and expansion
            leaf = self.select(root)
            # simulation
            simulation_result = self.rollout(leaf)
            # backpropagation
            self.backpropagate(leaf, simulation_result)
        # from next best state get move coordinates
        selected = self.best_child(root)
        for j in range(6):
            for i in range(7):
                if selected.board[j][i] != root.board[j][i]:
                    return j, i

    # Node traversal
    def select(self, node):
        # if all children of node has been expanded
        # select best one according to uct value
        while self.fully_expanded(node):
            tmp = self.select_uct(node)
            # if select_uct returns back the node break
            if tmp == node:
                break
            # if not, keep exploring the tree
            else:
                node = tmp
        # if node is terminal, return it
        if node.terminal:
            return node
        else:
            # expand node and return it for rollout
            node.add_child()
            if node.children:
                return self.pick_unvisited(node.children)
            else:
                return node

    # Return node with best uct value
    def select_uct(self, node):
        best_uct = -10000000
        best_node = None
        for child in node.children:
            uct = (child.Q / child.N) + 2 * math.sqrt((math.log(node.N)) / child.N)
            if uct > best_uct:
                best_uct = uct
                best_node = child
        # Avoid error if node has no children
        if best_node is None:
            return node
        else:
            return best_node

    # Check if node is a leaf
    def fully_expanded(self, node):
        visited = True
        # max number of children a node can have
        if list(node.board[5]).count(0) == len(node.children):
            # check if every node has been visited
            for child in node.children:
                if child.N == 0:
                    visited = False
            return visited
        else:
            return False

    # Policy for choosing unexplored nodes
    def pick_unvisited(self, children):
        for child in children:
            if child.N == 0:
                return child

    # Given a node, returns result of simulation
    def rollout(self, node):
        board = node.board
        turn = node.turn
        if not node.terminal:
            while (True):
                # switch turn
                if turn == 1:
                    turn = 2
                else:
                    turn = 1
                # get moves from current board
                moves = self.get_moves(board, turn)
                if moves:
                    # select next board randomly
                    board = random.choice(moves)
                    # check if state is terminal
                    terminal = self.result(board)
                    if terminal != 0:
                        # print("rollout", board)
                        return terminal
                # with no moves left return result
                else:
                    return self.result(board)
        else:
            # if node is already terminal return result
            return self.result(board)

    # Return all possible next states
    def get_moves(self, board, turn):
        moves = list()
        for i in range(7):
            if board[5, i] == 0:
                for j in range(6):
                    if board[j, i] == 0:
                        tmp = board.copy()
                        if turn == 1:
                            tmp[j, i] = 2
                        else:
                            tmp[j, i] = 1
                        moves.append(tmp)
                        break
        return moves

    # Get result score from board
    def result(self, board):
        winner = None
        # check rows
        for y in range(6):
            row = list(board[y, :])
            for x in range(4):
                if row[x:x + 4].count(row[x]) == 4:
                    if row[x] != 0:
                        winner = row[x]
        # check columns
        for x in range(7):
            col = list(board[:, x])
            for y in range(3):
                if col[y:y + 4].count(col[y]) == 4:
                    if col[y] != 0:
                        winner = col[y]
        # check right diagonals
        points = [(3, 0), (4, 0), (3, 1), (5, 0), (4, 1), (3, 2),
                  (5, 1), (4, 2), (3, 3), (5, 2), (4, 3), (5, 3)]
        for point in points:
            diag = list()
            for k in range(4):
                diag.append(board[point[0] - k, point[1] + k])
            if diag.count(1) == 4 or diag.count(2) == 4:
                winner = diag[k]
        # check left diagonals
        points = [(5, 3), (5, 4), (4, 3), (5, 5), (4, 4), (3, 3),
                  (5, 6), (4, 5), (3, 4), (4, 6), (3, 5), (3, 6)]
        for point in points:
            diag = list()
            for k in range(4):
                diag.append(board[point[0] - k, point[1] - k])
            if diag.count(1) == 4 or diag.count(2) == 4:
                winner = diag[k]
        # Tie
        if winner is None:
            return 0
        else:
            # Win
            if self.symbol == winner:
                return 1
            # Defeat
            else:
                return -1

    # Resursive function to update number of visits
    # and score of each node from leaf to root
    def backpropagate(self, node, result):
        # add result when AI's turn
        if node.turn == self.symbol:
            node.Q += result
        # or else subtract it
        else:
            node.Q -= result
        # increment visit number by 1
        node.N += 1
        # stop if node is root
        if node.parent is None:
            return
        else:
            # call function recursively on parent
            self.backpropagate(node.parent, result)

    # Returns root child with largest number of visits
    def best_child(self, node):
        max_visit = 0
        best_node = None
        for child in node.children:
            if child.N > max_visit:
                max_visit = child.N
                best_node = child
        return best_node

class Node:

    # Class initialization
    def __init__(self, parent, board, turn):
        self.Q = 0  # sum of rollout outcomes
        self.N = 0  # number of visits
        self.parent = parent
        self.board = board
        # root is always opponent's turn
        if turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        # no children has been expanded yet
        self.children = []
        self.expanded = False
        self.terminal = self.check_terminal()

    # Check if node is a leaf
    def check_terminal(self):
        # check rows
        for y in range(6):
            row = list(self.board[y, :])
            for x in range(4):
                if row[x:x + 4].count(row[x]) == 4:
                    if row[x] != 0:
                        return True
        # check columns
        for x in range(7):
            col = list(self.board[:, x])
            for y in range(3):
                if col[y:y + 4].count(col[y]) == 4:
                    if col[y] != 0:
                        return True
        # check right diagonals
        points = [(3, 0), (4, 0), (3, 1), (5, 0), (4, 1), (3, 2),
                  (5, 1), (4, 2), (3, 3), (5, 2), (4, 3), (5, 3)]
        for point in points:
            diag = list()
            for k in range(4):
                diag.append(self.board[point[0] - k, point[1] + k])
            if diag.count(1) == 4 or diag.count(2) == 4:
                return True
        # check left diagonals
        points = [(5, 3), (5, 4), (4, 3), (5, 5), (4, 4), (3, 3),
                  (5, 6), (4, 5), (3, 4), (4, 6), (3, 5), (3, 6)]
        for point in points:
            diag = list()
            for k in range(4):
                diag.append(self.board[point[0] - k, point[1] - k])
            if diag.count(1) == 4 or diag.count(2) == 4:
                return True
        # no winner
        return False

    # Add child to node
    def add_child(self):
        # node already expanded
        if self.expanded:
            return
        # get board of every child
        child_board = list()
        for child in self.children:
            child_board.append(child.board)
        # find new child
        for i in range(7):
            if self.board[5, i] == 0:
                for j in range(6):
                    if self.board[j, i] == 0:
                        tmp = self.board.copy()
                        if self.turn == 1:
                            tmp[j, i] = 2
                            if child_board:
                                if not self.compare_children(tmp, child_board):
                                    self.children.append(Node(self, tmp, 1))
                                    return
                                else:
                                    break
                            else:
                                self.children.append(Node(self, tmp, 1))
                                return
                        else:
                            tmp[j, i] = 1
                            if child_board:
                                if not self.compare_children(tmp, child_board):
                                    self.children.append(Node(self, tmp, 2))
                                    return
                                else:
                                    break
                            else:
                                self.children.append(Node(self, tmp, 2))
                                return
        # no more children
        self.expanded = True
        return

    # True if children states are equal
    def compare_children(self, new_child, children):
        for child in children:
            if (new_child == child).all():
                return True
        return False


# Run this script to play Connect 4 against AI
# with graphics printed out on the console with ASCII characters
if __name__ == "__main__":

    # Begin new game
    while True:
        print("Choose Number of Your desired Opponent:")
        print("     1.MONTE CARLO 2.MINIMAX without purning 3.MINIMAX with purning")
        opp = int(input())
        # Classes declaration
        my_list = input('Enter board size: ').split()
        r_c = [int(item) for item in my_list]

        gameBoard = GameBoard(cpu=1, row=r_c[0], col=r_c[1])
        monteCarlo = MCTS(symbol=1, t=5)

        # Game loop
        while True:

            # Print out the updated game board
            gameBoard.show()

            # Check game over
            winner = gameBoard.check_win()
            if winner is not None:
                if winner == gameBoard.cpu:
                    print("\n\nCPU WON!!!")
                else:
                    print("\n\nYOU WON!!!")
                break
            else:
                if list(gameBoard.board.flatten()).count(0) == 0:
                    print("\n\nTIE!!!")
                    break

            # AI turn
            if gameBoard.turn == monteCarlo.symbol:
                if opp == 0:
                    # initialiaze root node
                    root = Node(parent=None, board=gameBoard.board, turn=monteCarlo.symbol)
                    # compute best move with monte carlo tree search
                    move = monteCarlo.compute_move(root)
                elif opp == 2:
                    game = ConnectSin(board_size=(r_c[0], r_c[1]), board=gameBoard.board, silent=False)
                    move = game.get_your_input()
                else:
                    PURNING = True
                    game = ConnectSin(board_size=(r_c[0], r_c[1]), board=gameBoard.board, silent=False)
                    move = game.get_your_input()

                # update game board
                gameBoard.board[move[0], move[1]] = monteCarlo.symbol
                gameBoard.switch_turn()
            # Human turn
            else:
                gameBoard.play()

        # Rematch
        print("\n\nDo you want to play again? [Yes/No]", end=" ")
        ans = input()
        if ans in ["yes"]:
            continue
        else:
            break
