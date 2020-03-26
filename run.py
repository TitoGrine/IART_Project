from zhed_board import ZhedBoard
from graph.graph import Graph
from puzzle_reader import get_puzzle
from datetime import datetime

puzzle = get_puzzle(16)
game_board = ZhedBoard.build_from_file(puzzle)
print(game_board)
start_timestamp = datetime.now()
graph = Graph(lambda node: node.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
node = graph.a_star(game_board)
end_timestamp = datetime.now()
print(node)
elapsed_time = end_timestamp-start_timestamp
print("Elapsed Time: " + str(elapsed_time) + "ms")
