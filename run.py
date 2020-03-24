from zhed_board import ZhedBoard
from graph.graph import Graph
board = [["1", ".", ".", "X"], [".", "1", ".", "."]]

game_board = ZhedBoard.build_from_file(board)
print(game_board)
graph = Graph(lambda node: node.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
node = graph.a_star(game_board)
print(node)
