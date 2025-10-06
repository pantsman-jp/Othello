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
