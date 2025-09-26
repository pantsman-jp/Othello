def init_board(n):
    """
    nxn の盤面を作る．
    n は6以上の偶数を想定する
    """
    xss = [[0] * n for _ in range(n)]
    div2 = n // 2
    div2_1 = div2 - 1
    xss[div2_1][div2] = xss[div2][div2_1] = 2
    xss[div2_1][div2_1] = xss[div2][div2] = 1
    return xss


def convert(n):
    """
    0 -> スペース
    1 -> ●（黒）
    2 -> ○（白）
    に変換
    """
    if n == 0:
        return " "
    if n == 1:
        return "●"
    if n == 2:
        return "○"


def print_board(board):
    """
    インデックス付きで盤面表示をする
    黒は ●，白は ○
    """
    print("  " + " ".join(map(str, range(len(board)))))
    for i, xs in enumerate(board):
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
    範囲外のものは除く
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
    注目マス(y,x)から，ベクトル(vy,vx)方向のマスを列挙する
    （注目マスは含まない）
    """
    pos = [y + vy, x + vx]
    if all_in_range(n, pos):
        return [pos] + get_line(n, *pos, vy, vx)
    return []


def get_all_direction():
    """return [[vy, vx], ...]"""
    return [[vy, vx] for vx in [-1, 0, 1] for vy in [-1, 0, 1] if not vy == vx == 0]


def opponent(player):
    if player == 1:
        return 2
    return 1


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


def count_stones(board):
    """return [黒石の数, 白石の数]"""
    black, white = 0, 0
    for xs in board:
        for x in xs:
            if x == 1:
                black += 1
            elif x == 2:
                white += 1
    return [black, white]


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


def who(player):
    return {1: "黒(●)", 2: "白(○)"}[player]


def play_game():
    """黒(●)=1、白(○)=2"""
    n = int(input("盤面のサイズを入力（4以上の偶数）: "))
    if (n < 4) or (n % 2 == 1):
        print("4以上の偶数を入力してください。")
        play_game()
    board = init_board(n)
    player = 1
    while not game_over(board):
        print("現在の盤面")
        print_board(board)
        print(who(player) + " の手番です。")
        moves = legal_moves(board, player)
        if moves == []:
            print("打てる手がないのでパスします。")
            player = opponent(player)
            continue
        while True:
            try:
                print("どこに石をおきますか？")
                y = int(input("y座標(行): "))
                x = int(input("x座標(列): "))
                print("---------------------------")
                if [y, x] in moves:
                    break
                print("合法手ではありません。もう一度入力してください。")
            except ValueError:
                print("有効な整数を入力してください。")
        apply_move(board, y, x, player)
        player = opponent(player)
    black, white = count_stones(board)
    print_board(board)
    print("ゲーム終了! 黒:", black, " 白:", white)
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
        print(is_legal_move(board, 2, 3, 1))


if __name__ == "__main__":
    test(debug=False)
    play_game()
