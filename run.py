from zhed_board import ZhedBoard
from graph.graph import Graph
from puzzle_reader import read_file
from datetime import datetime
from heuristics import heuristics
import sys


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


algorithms = {
    "dfs": lambda graph, board: graph.dfs(board),
    "bfs": lambda graph, board: graph.bfs(board),
    "iterative_dfs": lambda graph, board: graph.iterative_dfs(board),
    "uniform_cost": lambda graph, board: graph.uniform_cost(board),
    "a_star": lambda graph, board: graph.a_star(board)
}


def run_puzzle(num, algorithm_type):
    puzzle = read_file(num)
    print(num, end=",")
    game_board = ZhedBoard.build_from_file(puzzle)
    start_timestamp = datetime.now()
    graph = Graph(lambda node: node.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
    node = algorithms[algorithm_type](graph, game_board)
    end_timestamp = datetime.now()
    elapsed_time = end_timestamp - start_timestamp
    print(elapsed_time.microseconds)
    return node


def run_statistics(puzzles):
    for filename, heuristic in heuristics.items():
        sys.stdout = open(filename + ".csv", "w")
        print("Puzzle Number, Expanded Nodes, Elapsed Time")
        ZhedBoard.heuristics_function = heuristic
        for i in puzzles:
            run_puzzle(i, "a_star")


run_statistics([1, 2, 3, 4])
