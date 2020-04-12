class Node:
    def __init__(self, state, parent=None, heuristics=False):
        """ Constructor
        :param state: current node state
        :param parent: parent's node
        :param heuristics: if it is the using heuristics or not
        """
        self.heuristics = heuristics
        self.parent = parent
        self.state = state

    def __lt__(self, other):
        """ Less than operator definition
        :param other: the other node
        :return: the smallest
        """
        return self.evaluate_node() < other.evaluate_node()

    def evaluate_node(self):
        """ Evaluation of a node
        :return: the current cost with the heuristic or not
        """
        return self.state.cost_value + (self.state.heuristics_value if self.heuristics else 0)
