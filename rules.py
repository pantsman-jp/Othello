from utils import get_all_direction, get_line, opponent, in_range


def valid_directions(board, y, x, player):
    """
    player が y,x に置いたとき，
    相手の石をひっくり返せる方向ベクトルのリストを返す
    """
    n = len(board)
    dirs = []
    for [vy, vx] in get_all_direction():
        flipped = []
        for [yy, xx] in get_line(n, y, x, vy, vx):
            if board[yy][xx] == opponent(player):
                flipped += [[yy, xx]]
            elif board[yy][xx] == player:
                if flipped != []:
                    dirs += [[vy, vx]]
                break
            else:
                break
    return dirs


def is_legal_move(board, y, x, player):
    """player が位置 y,x に石を置こうとするのは合法か？"""
    n = len(board)
    if (not in_range(n, y)) or (not in_range(n, x)):
        return False
    if board[y][x] != 0:
        return False
    return valid_directions(board, y, x, player) != []


def legal_moves(board, player):
    """合法手の列挙"""
    n = len(board)
    return [
        [y, x] for y in range(n) for x in range(n) if is_legal_move(board, y, x, player)
    ]


def game_over(board):
    return all(legal_moves(board, player) == [] for player in [1, 2])


def apply_move(board, y, x, player):
    """
    player の石を y,x に置き，
    ひっくり返せる相手の石を全てひっくり返す
    """
    board[y][x] = player
    n = len(board)
    for [vy, vx] in valid_directions(board, y, x, player):
        for [yy, xx] in get_line(n, y, x, vy, vx):
            if board[yy][xx] == player:
                break
            board[yy][xx] = player
    return board
