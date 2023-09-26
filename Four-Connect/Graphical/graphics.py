import pygame

# Screen resolution
WIN_SIZE = (W_WIDTH, W_HEIGHT) = (800, 600)


class GameGraphics:
    # Class initialization
    def __init__(self, win_size, surface):
        self.win_size = win_size
        self.surface = surface

    # Draw background elements
    def draw_background(self, speed):
        self.surface.fill((255, 255, 255))

    # Draw game board and players' pieces
    def draw_board(self, board):
        radius = 30
        w_space = 41
        h_space = 13
        shift = 7
        # Draw frame shadow
        frame = pygame.Surface((752, 451))
        frame.fill((50, 50, 50))
        frame.set_colorkey((255, 255, 255))
        for i in range(7):
            for j in range(6):
                pos = (w_space + radius + i * (w_space + 2 * radius), h_space + radius + j * (h_space + 2 * radius))
                pygame.draw.circle(frame, (255, 255, 255), pos, radius)
        self.surface.blit(frame, (w_space / 2 + shift, 125 - shift))
        outline = pygame.Surface(self.win_size)
        outline.fill((255, 255, 255))
        outline.set_colorkey((255, 255, 255))
        points1 = ((0, shift), (shift, 0), (752 + shift, 0), (752, shift))
        points2 = ((752 + shift, 0), (752 + shift, 451), (752, 451 + shift), (752, shift))
        pygame.draw.polygon(outline, (50, 50, 50), points1)
        pygame.draw.polygon(outline, (85, 107, 47), points2)
        self.surface.blit(outline, (20, 117))
        # Draw frame
        frame = pygame.Surface((752, 451))
        frame.fill((0, 100, 0))
        frame.set_colorkey((255, 255, 255))
        for i in range(7):
            for j in range(6):
                pos = (w_space + radius + i * (w_space + 2 * radius), h_space + radius + j * (h_space + 2 * radius))
                pygame.draw.circle(frame, (255, 255, 255), pos, radius)
        # Draw pieces
        for row in range(6):
            for col in range(7):
                if board[5 - row, col] == 1:
                    pos = (
                        w_space + radius + col * (w_space + 2 * radius),
                        h_space + radius + row * (h_space + 2 * radius))
                    pygame.draw.circle(frame, (220, 0, 0), pos, radius)
                elif board[5 - row, col] == 2:
                    pos = (
                        w_space + radius + col * (w_space + 2 * radius),
                        h_space + radius + row * (h_space + 2 * radius))
                    pygame.draw.circle(frame, (238, 219, 4), pos, radius)
        # Blit surface to screen
        self.surface.blit(frame, (w_space / 2, 125))

    # Column highlight selector
    def draw_select(self, column, turn):
        radius = 30
        w_space = 41
        h_space = 13
        shift = 3
        # Draw colo(220, 0, 0) piece based on player turn
        if turn == 1:
            surf = pygame.Surface((752, 451))
            surf.set_colorkey((0, 0, 0))
            pos = (w_space + radius + (column - 1) * (w_space + 2 * radius), h_space + radius)
            pygame.draw.circle(surf, (120, 0, 0), pos, radius)
            self.surface.blit(surf, (w_space / 2 + shift, 18 - shift))
            surf = pygame.Surface((752, 451))
            surf.set_colorkey((0, 0, 0))
            pos = (w_space + radius + (column - 1) * (w_space + 2 * radius), h_space + radius)
            pygame.draw.circle(surf, (220, 0, 0), pos, radius)
            self.surface.blit(surf, (w_space / 2, 18))
        elif turn == 2:
            surf = pygame.Surface((752, 451))
            surf.set_colorkey((0, 0, 0))
            pos = (w_space + radius + (column - 1) * (w_space + 2 * radius), h_space + radius)
            pygame.draw.circle(surf, (138, 119, 0), pos, radius)
            self.surface.blit(surf, (w_space / 2 + shift, 18 - shift))
            surf = pygame.Surface((752, 451))
            surf.set_colorkey((0, 0, 0))
            pos = (w_space + radius + (column - 1) * (w_space + 2 * radius), h_space + radius)
            pygame.draw.circle(surf, (238, 219, 4), pos, radius)
            self.surface.blit(surf, (w_space / 2, 18))

    # Draw game over screen
    def gameover_screen(self, winner, select):
        shift = 3
        surf = pygame.Surface(self.win_size)
        font = pygame.font.SysFont("Futura", 50)
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))
        # Draw menu window
        pygame.draw.rect(surf, (0, 100, 0), (100, 150, 600, 300))
        pygame.draw.rect(surf, (238, 219, 4), (200, 380, 120, 40))
        pygame.draw.rect(surf, (220, 0, 0), (480, 380, 120, 40))
        # Draw window shadow
        pygame.draw.polygon(surf, (50, 50, 50), (
            (100, 150), (100 + shift, 150 - shift), (700 + shift, 150 - shift), (700 + shift, 450 - shift), (700, 450),
            (700, 150)))
        pygame.draw.polygon(surf, (50, 50, 50), (
            (200, 380), (200 + shift, 380 - shift), (320 + shift, 380 - shift), (320 + shift, 420 - shift), (320, 420),
            (320, 380)))
        pygame.draw.polygon(surf, (50, 50, 50), (
            (480, 380), (480 + shift, 380 - shift), (600 + shift, 380 - shift), (600 + shift, 420 - shift), (600, 420),
            (600, 380)))
        # Draw answear selector
        if select == 1:
            pygame.draw.rect(surf, (255, 255, 255), (200, 380, 120, 40), 3)
        elif select == 2:
            pygame.draw.rect(surf, (255, 255, 255), (480, 380, 120, 40), 3)
        # Draw separator line
        pygame.draw.rect(surf, (255, 255, 255), (150, 260, 500, 5))
        self.surface.blit(surf, (0, 0))
        # Draw text
        if winner == 1:
            champion = font.render("AI is the winner!".format(winner), True, (255, 255, 255))
            self.surface.blit(champion, (180, 182))
        elif winner == 2:
            champion = font.render("Human won against the machine!".format(winner), True, (255, 255, 255))
            self.surface.blit(champion, (125, 182))
        else:
            champion = font.render("Match tied!".format(winner), True, (255, 255, 255))
            self.surface.blit(champion, (185, 182))
        rematch = font.render("Rematch?", True, (255, 255, 255))
        yes = font.render("YES", True, (255, 255, 255))
        no = font.render("NO", True, (255, 255, 255))
        yes_s = font.render("YES", True, (50, 50, 50))
        no_s = font.render("NO", True, (50, 50, 50))
        self.surface.blit(rematch, (320, 310))
        self.surface.blit(yes_s, (225, 383))
        self.surface.blit(no_s, (517, 383))
        self.surface.blit(yes, (223, 385))
        self.surface.blit(no, (515, 385))

    def opponent_selection(self, select):
        shift = 3
        surf = pygame.Surface(self.win_size)
        font = pygame.font.SysFont("Futura", 50)
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))
        # Draw menu window
        pygame.draw.rect(surf, (0, 100, 0), (100, 150, 600, 300))
        pygame.draw.rect(surf, (238, 219, 4), (200, 380, 120, 40))
        pygame.draw.rect(surf, (220, 0, 0), (480, 380, 120, 40))
        # Draw window shadow
        pygame.draw.polygon(surf, (50, 50, 50), (
            (100, 150), (100 + shift, 150 - shift), (700 + shift, 150 - shift), (700 + shift, 450 - shift), (700, 450),
            (700, 150)))
        pygame.draw.polygon(surf, (50, 50, 50), (
            (200, 380), (200 + shift, 380 - shift), (320 + shift, 380 - shift), (320 + shift, 420 - shift), (320, 420),
            (320, 380)))
        pygame.draw.polygon(surf, (50, 50, 50), (
            (480, 380), (480 + shift, 380 - shift), (600 + shift, 380 - shift), (600 + shift, 420 - shift), (600, 420),
            (600, 380)))
        # Draw answear selector
        if select == 1:
            pygame.draw.rect(surf, (255, 255, 255), (200, 380, 120, 40), 3)
        elif select == 2:
            pygame.draw.rect(surf, (255, 255, 255), (480, 380, 120, 40), 3)
        # Draw separator line
        pygame.draw.rect(surf, (255, 255, 255), (150, 260, 500, 5))
        self.surface.blit(surf, (0, 0))
        # Draw text

        champion = font.render("Do you want to play ", True, (255, 255, 255))
        self.surface.blit(champion, (180, 182))
        rematch = font.render("Multiplayer?", True, (255, 255, 255))
        yes = font.render("Yes", True, (255, 255, 255))
        no = font.render("No", True, (255, 255, 255))
        yes_s = font.render("Yes", True, (50, 50, 50))
        no_s = font.render("No", True, (50, 50, 50))
        self.surface.blit(rematch, (320, 310))
        self.surface.blit(yes_s, (225, 383))
        self.surface.blit(no_s, (517, 383))
        self.surface.blit(yes, (223, 385))
        self.surface.blit(no, (515, 385))

    def multiplayer_selection(self, select):
        shift = 3
        surf = pygame.Surface(self.win_size)
        font = pygame.font.SysFont("Futura", 50)
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))
        # Draw menu window
        pygame.draw.rect(surf, (0, 100, 0), (100, 150, 600, 300))
        pygame.draw.rect(surf, (238, 219, 4), (200, 380, 120, 40))
        pygame.draw.rect(surf, (220, 0, 0), (480, 380, 120, 40))
        # Draw window shadow
        pygame.draw.polygon(surf, (50, 50, 50), (
            (100, 150), (100 + shift, 150 - shift), (700 + shift, 150 - shift), (700 + shift, 450 - shift), (700, 450),
            (700, 150)))
        pygame.draw.polygon(surf, (50, 50, 50), (
            (200, 380), (200 + shift, 380 - shift), (320 + shift, 380 - shift), (320 + shift, 420 - shift), (320, 420),
            (320, 380)))
        pygame.draw.polygon(surf, (50, 50, 50), (
            (480, 380), (480 + shift, 380 - shift), (600 + shift, 380 - shift), (600 + shift, 420 - shift), (600, 420),
            (600, 380)))
        # Draw answear selector
        if select == 1:
            pygame.draw.rect(surf, (255, 255, 255), (200, 380, 120, 40), 3)
        elif select == 2:
            pygame.draw.rect(surf, (255, 255, 255), (480, 380, 120, 40), 3)
        # Draw separator line
        pygame.draw.rect(surf, (255, 255, 255), (150, 260, 500, 5))
        self.surface.blit(surf, (0, 0))
        # Draw text

        champion = font.render("Do you want to play", True, (255, 255, 255))
        self.surface.blit(champion, (180, 182))
        rematch = font.render("multiplayer?", True, (255, 255, 255))
        yes = font.render("Yes", True, (255, 255, 255))
        no = font.render("No", True, (255, 255, 255))
        yes_s = font.render("Yes", True, (50, 50, 50))
        no_s = font.render("No", True, (50, 50, 50))
        self.surface.blit(rematch, (320, 310))
        self.surface.blit(yes_s, (225, 383))
        self.surface.blit(no_s, (517, 383))
        self.surface.blit(yes, (223, 385))
        self.surface.blit(no, (515, 385))
