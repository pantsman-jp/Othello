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


def get_all_direction():
    """return [[vy, vx], ...]"""
    return [
        [vy, vx] for vx in [-1, 0, 1] for vy in [-1, 0, 1] if not [vy, vx] == [0, 0]
    ]


def opponent(player):
    return [2, 1][player - 1]


# TODO Fix
def valid_directions(board, y, x, player):
    """
    player が (y,x) に置いたとき，相手の石をひっくり返せる方向ベクトルのリストを返す
    """
    n = len(board)
    ret = []
    for [vy, vx] in get_all_direction():
        line = get_line(n, y, x, vy, vx)
        if line == []:
            continue
        if board[line[0][0]][line[0][1]] != opponent(player):
            continue
        stones = [board[yy][xx] for [yy, xx] in line]
        if (player in stones) and (stones.index(player) >= 1):
            ret += [[vy, vx]]
    return ret


def is_legal_move(board, y, x, player):
    """player が位置 y, x に石を置こうとするのは合法か？"""
    return valid_directions(board, y, x, player) != []


def legal_moves(board, player):
    """合法手の列挙"""
    n = len(board)
    return [
        [y, x] for y in range(n) for x in range(n) if is_legal_move(board, y, x, player)
    ]


def game_over(board):
    return all(legal_moves(board, player) == [] for player in [1, 2])


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


def apply_move(board, y, x, player):
    """
    player の石を y, x に置き、ひっくり返せる相手の石を全てひっくり返す。
    player の石が y, x に置かれることは is_legal_move で合法だとする。
    """
    board[y][x] = player
    n = len(board)
    for [vy, vx] in valid_directions(board, y, x, player):
        for [yy, xx] in get_line(n, y, x, vy, vx):
            board[yy][xx] = player
    return board


def who(player):
    return {1: "黒(○)", 2: "白(●)"}[player]


def play_game():
    """黒(○)は 1 白(●)は 2"""
    n = int(input("盤面のサイズを入力（6以上の偶数）: "))
    board = init_board(n)
    player = 1
    while not game_over(board):
        print_board(board)
        print(who(player) + " の手番")
        moves = legal_moves(board, player)
        if moves == []:
            print("打てる手がないのでパスします。")
            player = opponent(player)
            continue
        while True:
            try:
                print("どこに石をおきますか")
                y = int(input("y座標(行): "))
                x = int(input("x座標(列): "))
                if [y, x] in moves:
                    break
                print("合法手ではありません。もう一度入力してください。")
            except ValueError:
                print("数値を入力してください。")
        apply_move(board, y, x, player)
        player = opponent(player)
    black, white = count_stones(board)
    print_board(board)
    print("ゲーム終了! 黒: ", black, "白: ", white)
    if black > white:
        print("黒の勝ち!")
    elif white > black:
        print("白の勝ち!")
    else:
        print("引き分け!")


def test(debug):
    if debug:
        n = 8
        board = init_board(n)
        print_board(board)
        # print(get_neighbors(n, 9, 9))
        # print(get_line(n, 0, 0, 1, 1))
        # print(count_stones(board))
        print(is_legal_move(board, 3, 2, 1))


test(debug=False)
play_game()
