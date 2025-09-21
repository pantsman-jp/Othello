debug = True


def init_board(n):
    """
    nxn の盤面を作る。
    n は6以上の偶数を想定する
    """
    xss = [[0] * n for _ in range(n)]
    div2 = n // 2
    div2_1 = div2 - 1
    xss[div2_1][div2] = xss[div2][div2_1] = 1
    xss[div2_1][div2_1] = xss[div2][div2] = 2
    return xss


def convert(n):
    """
    0 -> スペース
    1 -> ●（白）
    2 -> ○（黒）
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
    インデックス付きで盤面表示をする
    白は ●、黒は ○
    """
    print("  " + " ".join(map(str, range(len(board)))))
    for [i, xs] in enumerate(board):
        print(str(i) + " " + " ".join(map(convert, xs)))


def in_range(n, m):
    """整数 m は 0 以上 n 未満か?"""
    return 0 <= m < n


def all_in_range(n, pos):
    """座標のリスト pos の各要素は in_range を満たすか?"""
    return all(in_range(n, p) for p in pos)


def get_neighbors(n, y, x):
    """
    注目マスの8近傍の座標を返す
    n は盤面の一辺の長さ
    8x8 の範囲外のものは除く
    """
    ret = []
    for j in range(-1, 2):
        for i in range(-1, 2):
            if (j == 0) and (i == 0):
                continue
            pos = [y + j, x + i]
            if all_in_range(n, pos):
                ret += [pos]
    return ret


def get_line(n, y, x, vy, vx):
    """
    注目マス(y,x)から、ベクトル(vy,vx)方向のマスを列挙する
    （注目マスは含まない）
    n は盤面の一辺の長さ
    """
    pos = [y + vy, x + vx]
    if all_in_range(n, pos):
        return [pos] + get_line(n, *pos, vy, vx)
    return []


def opponent(player):
    return [2, 1][player - 1]


# TODO
def is_legal_move(board, y, x, player):
    if board[y][x] != 0:
        return False


def count_stones(board):
    """return [黒石の数, 白石の数]"""
    ret = [0, 0]
    for xs in board:
        for x in xs:
            if x == 0:
                pass
            else:
                ret[x - 1] += 1
    return ret


def game_over(board):
    return sum(count_stones(board)) == len(board) ** 2


def test(debug):
    if debug:
        n = 8
        board = init_board(n)
        print_board(board)
        # print(get_neighbors(n, 9, 9))
        # print(get_line(n, 0, 0, 1, 1))
        print(count_stones(board))


test(debug)
