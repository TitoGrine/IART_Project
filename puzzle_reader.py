import zhed_board


def get_puzzle(number):
    board = read_file(number)
    padded_board = padd_board(board)

    return padded_board


def read_file(number):
    missing_zeros = 3 - len(str(number))
    filename = "puzzles/" + ("0" * missing_zeros) + str(number) + ".txt"
    file = open(filename, 'r')

    lines = file.readlines()

    board = []

    for y in range(len(lines)):
        board.append(lines[y][0:-1])

    return board


def padd_board(board):
    max_length = max(len(board[0]) - 1, len(board))
    side_length = max_length + 2
    x_padding = round((max_length - (len(board[0]) - 1)) / 2) + 1
    y_padding = round((max_length - len(board)) / 2) + 1
    limit = len(board)
    padded_board = [] + [[zhed_board.BoardState.EMPTY] * side_length] * y_padding

    for y in range(side_length - y_padding):
        if y < limit:
            row = [zhed_board.BoardState.EMPTY] * x_padding + board[y] + [zhed_board.BoardState.EMPTY] * x_padding
        else:
            row = [zhed_board.BoardState.EMPTY] * side_length

        padded_board.append(row)

    return padded_board


def padd_raw_board(board):
    max_length = max(len(board[0]) - 1, len(board))
    side_length = max_length + 2
    x_padding = round((max_length - (len(board[0]) - 1)) / 2) + 1
    y_padding = round((max_length - len(board)) / 2) + 1
    limit = len(board)
    padded_board = [] + [''.join(['.'] * side_length)] * y_padding

    for y in range(side_length - y_padding):
        if y < limit:
            row = ''.join(['.'] * x_padding) + board[y] + ''.join(['.'] * x_padding)
        else:
            row = ''.join(['.'] * side_length)

        padded_board.append(row)

    return padded_board

def get_boards_list(main_node):
    boards = []
    node = main_node

    while True:
        boards.append(node.state)
        if node.parent == None:
            break
        else:
            node = node.parent

    boards.reverse()

    return boards
