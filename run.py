from zhed_board import ZhedBoard
from graph.graph import Graph
from puzzle_reader import get_puzzle

puzzle = get_puzzle(10)
game_board = ZhedBoard.build_from_file(puzzle)
print(game_board)
graph = Graph(lambda node: node.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
node = graph.a_star(game_board)
print(node)
