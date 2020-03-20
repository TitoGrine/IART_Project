from collections import defaultdict
from queue import PriorityQueue


class Graph:

    # Constructor
    def __init__(self, validation_function, adding_edges, limit):

        # default dictionary to store graph
        self.limit = limit
        self.graph = defaultdict(list)
        self.adding_edges = adding_edges
        self.validation_function = validation_function

    # function to add an edge to graph
    def add_edge(self, u, v):
        self.graph[u].append(v)

    def __run_graph(self, s, function):

        # Mark all the vertices as not visited
        visited = defaultdict(bool)

        # Create a queue for BFS
        queue = [s]

        # Mark the source node as
        # visited and enqueue it
        visited[s] = True
        finished = True
        n = 0
        while finished:

            # Dequeue a vertex from
            # queue and print it

            s = queue.pop(0)
            print(s, end=" ")
            for i in self.adding_edges(s):
                self.add_edge(s, i)
                # Get all adjacent vertices of the
                # dequeued vertex s. If a adjacent
                # has not been visited, then mark it
                # visited and enqueue it
            for i in self.graph[s]:
                if self.validation_function(s):
                    finished = False
                elif not visited[i]:
                    function(i, queue, visited, n)
            n += 1

    def __shortest_path(self, s, function):

        # Create a queue for BFS
        queue = PriorityQueue()
        queue.put(s)

        # Mark the source node as
        # visited and enqueue it
        finished = True
        n = 0
        while finished:

            # Dequeue a vertex from
            # queue and print it

            s = queue.get()
            print(s, end=" ")
            for i in self.graph[s]:
                if self.validation_function(s):
                    finished = False
                else:
                    function(i, queue)
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
    def __add_to_queue(i, queue):
        queue.put(queue, i)

    def bfs(self, s):
        self.__run_graph(s, self.__bfs)

    def dfs(self, s):
        self.__run_graph(s, self.__dfs)

    def iterative_dfs(self, s):
        self.__run_graph(s, self.__iterative)

    def shortest_path(self, s):
        self.__shortest_path(s, self.__add_to_queue)
