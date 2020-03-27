from zhed_board import ZhedBoard
from graph.graph import Graph
from puzzle_reader import read_file
from datetime import datetime

puzzle = read_file(16)
game_board = ZhedBoard.build_from_file(puzzle)
print(game_board)
start_timestamp = datetime.now()
graph = Graph(lambda node: node.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
node = graph.a_star(game_board)
end_timestamp = datetime.now()
print(node)
elapsed_time = end_timestamp - start_timestamp
print("Elapsed Time: " + str(elapsed_time) + "ms")


def get_boards_list(main_node):
    boards = []
    node = main_node

    while True:
        boards.append(node.state.board_state)
        if node.parent == None:
            break
        else:
            node = node.parent

    boards.reverse()

    return boards


def run_puzzle(puzzle):
    game_board = ZhedBoard.build_from_file(puzzle)
    graph = Graph(lambda node: node.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
    node = graph.a_star(game_board)

    return get_boards_list(node)
