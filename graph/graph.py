from collections import defaultdict
from queue import PriorityQueue
from graph.node import Node


class Graph:

    # Constructor
    def __init__(self, validation_function, adding_edges, limit=15):

        # default dictionary to store graph
        self.limit = limit
        self.graph = defaultdict(list)
        self.adding_edges = adding_edges
        self.validation_function = validation_function

    # function to add an edge to graph
    def add_edge(self, u, v):
        self.graph[u].append(Node(v, parent=u, heuristics=False))

    def __run_graph(self, s, function):

        # Mark all the vertices as not visited
        visited = defaultdict(bool)

        # Create a queue for BFS
        queue = [Node(s, heuristics=False)]

        # Mark the source node as
        # visited and enqueue it
        visited[s] = True
        n = 0
        while True:

            # Dequeue a vertex from
            # queue and print it
            if len(queue) == 0:
                print("Didn't find a solution! Stopping...")
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
                    return s
                elif not visited[i]:
                    function(i, queue, visited, n)
            n += 1

    def __shortest_path(self, s, function):

        # Create a queue for BFS
        queue = PriorityQueue()
        queue.put(Node(s))

        # Mark the source node as
        # visited and enqueue it
        n = 0
        while True:

            # Dequeue a vertex from
            # queue and print it
            if len(queue.queue) == 0:
                print("\nDidn't find a solution! Stopping...")
                break

            s = queue.get()
            # if s.state.move is not None:
            #     print("expanded " + str(s.state.move.starting_block) + str(s.state.move.move))
            for i in self.adding_edges(s):
                if self.validation_function(i):
                    return Node(i, parent=s)
                else:
                    function(i, s, queue)
            n += 1

    @staticmethod
    def __bfs(i, queue, visited, _):
        queue.append(i)
        visited[i] = True

    @staticmethod
    def __dfs(i, queue, visited, _):
        queue.insert(0, i)
        visited[i] = True

    def __iterative(self, i, queue, visited, n):
        if n % self.limit == 0:
            queue.append(i)
        else:
            queue.insert(0, i)
        visited[i] = True
        return True

    @staticmethod
    def __dijkstra(v, u, queue):
        queue.put(Node(v, parent=u, heuristics=False))

    @staticmethod
    def __a_star(v, u, queue):
        queue.put(Node(v, parent=u, heuristics=True))

    def bfs(self, s):
        return self.__run_graph(s, self.__bfs)

    def dfs(self, s):
        return self.__run_graph(s, self.__dfs)

    def iterative_dfs(self, s):
        return self.__run_graph(s, self.__iterative)

    def dijkstra(self, s):
        return self.__shortest_path(s, self.__dijkstra)

    def a_star(self, s):
        return self.__shortest_path(s, self.__a_star)
