class Node:
    def __init__(self, state, parent=None, heuristics=False):
        self.heuristics = heuristics
        self.parent = parent
        self.state = state

    def __lt__(self, other):
        return self.evaluate_node() < other.evaluate_node()

    def evaluate_node(self):
        return self.state.cost() + (self.state.heuristics() if self.heuristics else 0)
