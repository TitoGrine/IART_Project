from zhed.model.game_state import *

heuristics = {
    "all_heuristics": lambda board, goal: nearest_dist(board) + nearest_goal(board, goal) + in_direction_of_goal(
        board) +
                                          benefit_outer_blocks(board, goal) + punish_bad_expansions(board, goal),
    "negative_distance": lambda board, goal: nearest_goal(board, goal) - nearest_dist(board) + in_direction_of_goal(
        board) +
                                             benefit_outer_blocks(board, goal) + punish_bad_expansions(board, goal),
    "no_punishments": lambda board, goal: nearest_dist(board) + nearest_goal(board, goal) + in_direction_of_goal(
        board) +
                                          benefit_outer_blocks(board, goal),
    "constant_benefits": lambda board, goal: in_direction_of_goal(board) +
                                             benefit_outer_blocks(board, goal) + punish_bad_expansions(board, goal),
    "nearest": lambda board, goal: nearest_dist(board) + nearest_goal(board, goal)
}


def nearest_dist(board):
    """ Calculates the manhattan distance between the expanded block and the nearest goal
        :param board: current Board State
    """
    return board.manhattan(board.move.starting_block,
                           board.get_nearest(board.move.starting_block, board.align_numbered))


def nearest_goal(board, goal):
    """ Calculates the manhattan distance between the expanded block and
        the nearest block that is aligned with the goal
        :param board: current Board State
        :param goal: tuple with coordinates to the nearest goal
    """
    return board.manhattan(goal, board.move.finish_block)


def in_direction_of_goal(board):
    """ Values if any of the placed blocks are
        in the direction of the goal
        :param board: current Board State
    """
    value = 0
    for block in board.move.placed_blocks:
        x = block[1]
        y = block[0]
        for i in board.numbered:

            if i[0] == y:

                if abs(i[1] - x) <= board.board_state[i[0]][i[1]]:
                    value -= 10
            if i[1] == x:

                if abs(i[0] - y) <= board.board_state[i[0]][i[1]]:
                    value -= 10
    return value


def benefit_outer_blocks(board, nearest_goal):
    """ Punishes blocks closer to the goal
        :param board: current Board State
        :param nearest_goal: tuple with coordinates to the nearest goal
    """
    x, y = board.get_coordinates(board.move.starting_block)
    value = 0
    if len(board.numbered) > 2:
        # if in same row or column as goal, lessen priority
        if x == nearest_goal[1] or y == nearest_goal[0]:
            value += 9  # value subject to change

        # if expanding away from goal, lessen priority
        if board.move.move == BoardMove.LEFT and x < nearest_goal[1]:
            value += 7
        elif board.move.move == BoardMove.RIGHT and x > nearest_goal[1]:
            value += 7
        elif board.move.move == BoardMove.DOWN and y > nearest_goal[0]:
            value += 7
        elif board.move.move == BoardMove.UP and y < nearest_goal[0]:
            value += 7
    return value


def punish_bad_expansions(board, nearest_goal):
    """ Punishes moves that expand towards a direction
        where there are no useful blocks
        :param board: current Board State
        :param nearest_goal: tuple with coordinates to the nearest goal
    """
    x, y = board.get_coordinates(board.move.starting_block)
    edge_expand = True
    if board.move.move == BoardMove.LEFT:
        if nearest_goal[1] < x:
            edge_expand = False
        else:
            for i in board.numbered:
                if i[1] < x:
                    edge_expand = False
                    break
    elif board.move.move == BoardMove.RIGHT:
        if nearest_goal[1] > x:
            edge_expand = False
        else:
            for i in board.numbered:
                if i[1] > x:
                    edge_expand = False
                    break
    elif board.move.move == BoardMove.DOWN:
        if nearest_goal[0] > y:
            edge_expand = False
        else:
            for i in board.numbered:
                if i[0] > y:
                    edge_expand = False
                    break
    elif board.move.move == BoardMove.UP:
        if nearest_goal[0] < y:
            edge_expand = False
        else:
            for i in board.numbered:
                if i[0] < y:
                    edge_expand = False
                    break

    return 2000 if edge_expand else 0
