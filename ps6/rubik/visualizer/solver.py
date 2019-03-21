import rubik
from collections import deque


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 
    Assumes the rubik.quarter_twists move set.
    """
    print(rubik.perm_apply(rubik.F, rubik.I))
    print(rubik.I)
    return [rubik.U]


class Graph:
    @staticmethod
    def adj(u):
        adj_u = []
        if(u == rubik.I):
            return adj_u
        for move in rubik.quarter_twists:
            adj_u.append(rubik.perm_apply(move, u))
        return adj_u


class Node:
    def __init__(self, state, move):
        self.state = state
        self.move = move


class BFSResult:
    def __init__(self):
        self.level = {}
        self.parent = {}


rubik_moves = {rubik.F: 'rubik.F',
               rubik.Fi: 'rubik.Fi',
               rubik.L: 'rubik.L',
               rubik.Li: 'rubik.Li',
               rubik.U: 'rubik.U',
               rubik.Ui: 'rubik.Ui'}


def print_path(r, s, v):
    if v == s:
        return
    elif r.parent.get(v) is None:
        print("No path exists")
    else:
        print(rubik.quarter_twists_names[find_move(r.parent[v], v)])
        print_path(r, s, r.parent[v])


def find_move(u, v):
    for move in rubik.quarter_twists:
        if v == rubik.perm_apply(move, u):
            print move
            return move
    return -1


def bfs(s):
    r = BFSResult()
    r.parent = {s: None}
    r.level = {s: 0}

    queue = deque()
    queue.append(s)

    while queue:
        u = queue.popleft()
        # print(u)
        for n in Graph.adj(u):
            if n not in r.level:
                r.parent[n] = u
                r.level[n] = r.level[u] + 1
                queue.append(n)
    return r


if __name__ == '__main__':
    start = rubik.perm_apply(rubik.F, rubik.I)
    # start = rubik.perm_apply(rubik.U, start)
    # start = rubik.perm_apply(rubik.Ui, start)
    r = bfs(start)
    print(r.level)
    print_path(r, start, rubik.I)
