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
