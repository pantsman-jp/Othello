import pygame
from src.board import init_board, count_stones
from src.rules import game_over, legal_moves, apply_move
from src.utils import opponent

CELL_SIZE = 60
BOARD_COLOR = (0, 128, 0)
LINE_COLOR = (0, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
HINT_COLOR = (200, 200, 200)
WINDOW_MARGIN = 40


def draw_board(screen, board, player):
    n = len(board)
    screen.fill(BOARD_COLOR)
    for i in range(n + 1):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (WINDOW_MARGIN, WINDOW_MARGIN + i * CELL_SIZE),
            (WINDOW_MARGIN + n * CELL_SIZE, WINDOW_MARGIN + i * CELL_SIZE),
            2,
        )
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (WINDOW_MARGIN + i * CELL_SIZE, WINDOW_MARGIN),
            (WINDOW_MARGIN + i * CELL_SIZE, WINDOW_MARGIN + n * CELL_SIZE),
            2,
        )
    for y in range(n):
        for x in range(n):
            if board[y][x] == 1:
                pygame.draw.circle(
                    screen,
                    BLACK_COLOR,
                    (
                        WINDOW_MARGIN + x * CELL_SIZE + CELL_SIZE // 2,
                        WINDOW_MARGIN + y * CELL_SIZE + CELL_SIZE // 2,
                    ),
                    CELL_SIZE // 2 - 4,
                )
            elif board[y][x] == 2:
                pygame.draw.circle(
                    screen,
                    WHITE_COLOR,
                    (
                        WINDOW_MARGIN + x * CELL_SIZE + CELL_SIZE // 2,
                        WINDOW_MARGIN + y * CELL_SIZE + CELL_SIZE // 2,
                    ),
                    CELL_SIZE // 2 - 4,
                )
    moves = legal_moves(board, player)
    for [y, x] in moves:
        pygame.draw.circle(
            screen,
            HINT_COLOR,
            (
                WINDOW_MARGIN + x * CELL_SIZE + CELL_SIZE // 2,
                WINDOW_MARGIN + y * CELL_SIZE + CELL_SIZE // 2,
            ),
            CELL_SIZE // 6,
        )
    pygame.display.flip()


def get_cell(pos):
    x, y = pos
    x = (x - WINDOW_MARGIN) // CELL_SIZE
    y = (y - WINDOW_MARGIN) // CELL_SIZE
    return [y, x]


def who(player):
    return {1: "black(●)", 2: "white(○)"}[player]


def play_game_pygame():
    pygame.init()
    n = 8
    board = init_board(n)
    size = WINDOW_MARGIN * 2 + CELL_SIZE * n
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Othello")
    font = pygame.font.SysFont(None, 36)
    player = 1
    running = True
    while running:
        draw_board(screen, board, player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (not game_over(board)):
                y, x = get_cell(event.pos)
                moves = legal_moves(board, player)
                if [y, x] in moves:
                    apply_move(board, y, x, player)
                    player = opponent(player)
        if game_over(board):
            black, white = count_stones(board)
            msg = f"Game Set! Black: {black} White: {white} "
            if black > white:
                msg += "Black Win!"
            elif white > black:
                msg += "White Win!"
            else:
                msg += "Draw!"
            text = font.render(msg, True, (255, 0, 0))
            screen.blit(text, (10, 10))
            pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    play_game_pygame()
