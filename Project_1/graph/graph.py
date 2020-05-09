from collections import defaultdict
from queue import PriorityQueue
from graph.node import Node


class Graph:

    def __init__(self, validation_function, adding_edges, limit=15):
        """" Constructor
        :param validation_function: function to validate if it is a goal state
        :param adding_edges: function to run operators and get new states
        :param limit: limit to the iterative algorithm
        """
        # default dictionary to store graph
        self.limit = limit
        self.graph = defaultdict(list)
        self.adding_edges = adding_edges
        self.validation_function = validation_function

    def add_edge(self, u, v):
        """ Function to add an edge to graph
        :param u: child node
        :param v: parent node
        """
        self.graph[u].append(Node(v, parent=u, heuristics=False))

    def __run_graph(self, s, function):
        """ Runs a blind search algorithm
        :param s: starting node
        :param function: the specific blind search algorithm
        :return finishing node or None if not found
        """

        # Mark all the vertices as not visited
        visited = defaultdict(bool)

        # Create a queue for BFS
        queue = [Node(s, heuristics=False)]

        # Mark the source node as
        # visited and enqueue it
        visited[s] = True
        n = 0
        solution = None
        while True:

            # Dequeue a vertex from
            # queue and print it
            if len(queue) == 0:
                break

            s = queue.pop(0)
            for i in self.adding_edges(s):
                self.add_edge(s, i)
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if self.validation_function(i.state):
                    solution = s
                    break
                elif not visited[i]:
                    function(i, queue, visited, n)
            n += 1
        return solution

    def __shortest_path(self, s, function):
        """ Runs a directed search algorithm
        :param s: starting node
        :param function: the specific search algorithm
        :return finishing node or None if not found
        """

        # Create a queue for BFS
        queue = PriorityQueue()
        queue.put(Node(s))

        # Mark the source node as
        # visited and enqueue it
        n = 0
        solution = None
        finished = False
        while not finished:

            # Dequeue a vertex from
            # queue and print it
            if len(queue.queue) == 0:
                break

            s = queue.get()
            # if s.state.move is not None:
            #     print("expanded " + str(s.state.move.starting_block) + str(s.state.move.move))
            for i in self.adding_edges(s):
                if self.validation_function(i):
                    solution = Node(i, parent=s)
                    finished = True
                    break
                else:
                    function(i, s, queue)
            n += 1
        print("Nodes expanded: " + str(n))
        return solution

    @staticmethod
    def __bfs(i, queue, visited, _):
        """" Runs the bfs algorithm
        :param i: the current node
        :param queue: the current run's queue
        :param visited: boolean list
        """
        queue.append(i)
        visited[i] = True

    @staticmethod
    def __dfs(i, queue, visited, _):
        """" Runs the dfs algorithm
        :param i: the current node
        :param queue: the current run's queue
        :param visited: boolean list
        """
        queue.insert(0, i)
        visited[i] = True

    def __iterative(self, i, queue, visited, n):
        """" Runs the iterative dfs algorithm
        :param i: the current node
        :param queue: the current run's queue
        :param visited: boolean list
        :param n: current interation
        """
        if n % self.limit == 0:
            queue.append(i)
        else:
            queue.insert(0, i)
        visited[i] = True
        return True

    @staticmethod
    def __uniform_cost(v, u, queue):
        """" Runs the uniform cost algorithm
        :param v: the current node
        :param u: the parent node
        :param queue: the current run's priority queue
        """
        queue.put(Node(v, parent=u, heuristics=False))

    @staticmethod
    def __a_star(v, u, queue):
        """ Runs the A* algorithm
        :param v: the current node
        :param u: the parent node
        :param queue: the current run's priority queue
        """
        queue.put(Node(v, parent=u, heuristics=True))

    def bfs(self, s):
        """ Starts the bfs algorithm
        :param s: starting node
        :return: final node
        """
        return self.__run_graph(s, self.__bfs)

    def dfs(self, s):
        """ Starts the dfs algorithm
        :param s: starting node
        :return: final node
        """
        return self.__run_graph(s, self.__dfs)

    def iterative_dfs(self, s):
        """ Starts the iterative dfs algorithm
        :param s: starting node
        :return: final node
        """
        return self.__run_graph(s, self.__iterative)

    def uniform_cost(self, s):
        """ Starts the uniform cost algorithm
        :param s: starting node
        :return: final node
        """
        return self.__shortest_path(s, self.__uniform_cost)

    def a_star(self, s):
        """ Starts the A* algorithm
        :param s: starting node
        :return: final node
        """
        return self.__shortest_path(s, self.__a_star)
