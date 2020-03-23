from zhed_board import ZhedBoard
from graph.graph import Graph
board = [["1", "1", ".", "X"]]

game_board = ZhedBoard.build_from_file(board)
print(game_board)
graph = Graph(lambda node: node.state.is_goal, lambda node: ZhedBoard.get_all_operators(node.state))
node = graph.dijkstra(game_board)
print(node)
