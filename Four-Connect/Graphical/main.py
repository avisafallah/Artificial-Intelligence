from connect4_AI import GameBoard, MCTS, Node
from game_graphics import GameGraphics
from threading import Thread
from queue import Queue
import pygame
import os


# Screen resolution
WIN_SIZE = (W_WIDTH, W_HEIGHT) = (800, 600)

# Run this script to play Connect 4 against Monte Carlo AI
# with drawn game graphics in dedicated window
if __name__ == "__main__":

    # Initialize stuff
    os.system('cls')
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption('AvisaFallah AI Project Connect4')
    window = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()
    que = Queue()

    # Initialize game graphics
    graphics = GameGraphics(win_size=WIN_SIZE, surface=window)
    # Game over / continue


    # Begin new game
    while True:
        opp = 1
        selection = False
        while not selection:
            # Menu controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    # Move column selection to the right
                    if event.key == pygame.K_RIGHT:
                        if opp < 2:
                            opp += 1
                    # Move column selection to the left
                    elif event.key == pygame.K_LEFT:
                        if opp > 1:
                            opp -= 1
                    # Enter column and execute move
                    elif event.key == pygame.K_RETURN:
                        selection = True
                        break
                        # Start new game

            # Draw game over screen
            graphics.draw_background(speed=100)
            graphics.opponent_selection(opp)

            # Update stuff
            clock.tick(30)
            pygame.event.pump()
            pygame.display.flip()
        # Class declaration
        gameboard = GameBoard(cpu=1,row=6,col=7)
        montecarlo = MCTS(symbol=1, t=5)

        # Game variables
        winner = None
        select = 1

        # Monte carlo threads list
        threads = []

        # Game loop
        while True:

            # Check game over
            winner = gameboard.check_win()
            if winner is not None:
                pygame.time.wait(1500)
                break
            else:
                if list(gameboard.board.flatten()).count(0) == 0:
                    winner = 0
                    pygame.time.wait(1500)
                    break

            # Human turn
            if gameboard.turn != gameboard.cpu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        # Move column selection to the right
                        if event.key == pygame.K_RIGHT:
                            if select < 7:
                                select += 1
                        # Move column selection to the left
                        elif event.key == pygame.K_LEFT:
                            if select > 1:
                                select -= 1
                        # Enter column and execute move
                        elif event.key == pygame.K_RETURN:
                            if gameboard.board[5, select - 1] == 0:
                                gameboard.apply_move(column=select)

            # Monte Carlo turn
            else:
                if opp == 1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_over = True
                        if event.type == pygame.KEYDOWN:
                            # Move column selection to the right
                            if event.key == pygame.K_RIGHT:
                                if select < 7:
                                    select += 1
                            # Move column selection to the left
                            elif event.key == pygame.K_LEFT:
                                if select > 1:
                                    select -= 1
                            # Enter column and execute move
                            elif event.key == pygame.K_RETURN:
                                if gameboard.board[5, select - 1] == 0:
                                    gameboard.apply_move(column=select)
                # Start thinking
                if not threads:
                    if opp == 2:
                        # initialiaze root node
                        root = Node(parent=None, board=gameboard.board, turn=montecarlo.symbol)
                        # compute best move with monte carlo tree search
                        t = Thread(target=lambda q, arg1: q.put(montecarlo.compute_move(arg1)), args=(que, root))
                        t.start()
                        # Add t to current running threads
                        threads.append(t)
                if not que.empty():
                    # Remove thread
                    threads.pop()
                    # Get move from queue
                    move = que.get()
                    # Update board and switch turn
                    gameboard.board[move[0], move[1]] = montecarlo.symbol
                    gameboard.switch_turn()


            # Draw game graphics
            graphics.draw_background(speed=100)
            graphics.draw_board(board=gameboard.board)
            if gameboard.turn != gameboard.cpu:
                graphics.draw_select(column=select, turn=gameboard.turn)
            if gameboard.turn == gameboard.cpu and opp == 1:
                graphics.draw_select(column=select, turn=gameboard.turn)

            # Update stuff
            clock.tick(30)
            pygame.event.pump()
            pygame.display.flip()

        # Game over / continue
        select = 1
        new_game = False
        while not new_game:
            # Menu controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    # Move column selection to the right
                    if event.key == pygame.K_RIGHT:
                        if select < 2:
                            select += 1
                    # Move column selection to the left
                    elif event.key == pygame.K_LEFT:
                        if select > 1:
                            select -= 1
                    # Enter column and execute move
                    elif event.key == pygame.K_RETURN:
                        # Start new game
                        if select == 1:
                            new_game = True
                        elif select == 2:
                            exit()

            # Draw game over screen
            graphics.draw_background(speed=100)
            graphics.gameover_screen(winner, select)

            # Update stuff
            clock.tick(30)
            pygame.event.pump()
            pygame.display.flip()
