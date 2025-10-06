from board import init_board, print_board, count_stones
from rules import game_over, legal_moves, apply_move, is_legal_move
from utils import opponent


def who(player):
    return {1: "黒(●)", 2: "白(○)"}[player]


def play_game():
    """黒(●)=1、白(○)=2"""
    board = init_board(8)
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
