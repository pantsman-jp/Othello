def init_board():
    """
    8x8の盤面を作る。
    """
    xss = [[0] * 8 for _ in range(8)]
    xss[3][4] = xss[4][3] = 1
    xss[3][3] = xss[4][4] = 2
    return xss


def convert(n):
    """
    0 -> スペース
    1 -> ●
    2 -> ○
    に変換
    """
    if n == 0:
        return " "
    if n == 1:
        return "●"
    if n == 2:
        return "○"
    raise Exception("convert()", "引数が 0 か 1 か 2 ではありません", n)


def print_board(board):
    """
    盤面表示をする
    白は ●、黒は ○
    """
    print("  0 1 2 3 4 5 6 7")
    for [i, xs] in enumerate(board):
        print(str(i) + " " + " ".join(map(convert, xs)))


def get_neighbors(y, x):
    """
    注目マスの8近傍の座標を返す
    8x8 の範囲外のものは除く
    """
    ret = []
    for j in range(-1, 2):
        for i in range(-1, 2):
            if (j == 0) and (i == 0):
                continue
            new_y, new_x = y + j, x + i
            if (-1 < new_x < 8) and (-1 < new_y < 8):
                ret += [[new_y, new_x]]
    return ret


print_board(init_board())
print(get_neighbors(0, 0))
