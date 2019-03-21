import rubik
from collections import deque


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 
    Assumes the rubik.quarter_twists move set.
    """
    (front, f_q, back, b_q) = bfs(start, end)
    best_node = find_minimal_d(front, f_q, back, b_q)
    solution  = get_solution_path(front, back, best_node, start, end)
    return solution 


class Graph:
    @staticmethod
    def adj(u, dir):
        adj_u = []
        for move in rubik.quarter_twists:
                adj_u.append(rubik.perm_apply(move, u))
        return adj_u


class BFSResult:
    def __init__(self):
        self.level = {}
        self.parent = {}


def find_minimal_d(front, f_q, back, b_q):
    smallest = float("inf") 
    for node in f_q:
        if(node in b_q):
            temp = front.level.get(node) + back.level.get(node)  
            if(temp < smallest):
                smallest = temp
                best_node = node
    return best_node       
    
def get_solution_path(front, back, best_node, s, end):
    solution = []
    FORWARD = 1
    BACKWARD = 0
    v = best_node
    while(v!=s):
        solution.append(find_move(front.parent[v], v, FORWARD))
        v = front.parent[v]
    v = best_node
    while(v!=end):
        solution.append(find_move(back.parent[v], v, BACKWARD))
        v = back.parent[v]
    # for move in solution: 
    #     print(rubik.quarter_twists_names[move])
    return solution

def print_path(r, s, v):
    if v == s:
        return
    elif r.parent.get(v) is None:
        print("No path exists")
    else:
        rubik.quarter_twists_names(find_move(r.parent[v], v))
        print_path(r, s, r.parent[v])


def find_move(u, v, dir):
    for move in rubik.quarter_twists:
        if(dir):
            if v == rubik.perm_apply(move, u):
                return move
        else:
            if v == rubik.perm_apply(rubik.perm_inverse(move), u):
                return move
    return -1


def bfs(s, e):
    front = BFSResult()
    front.parent = {s: None}
    front.level = {s: 0}
    back = BFSResult()
    back.parent = {e: None}
    back.level = {e: 0}
    s_queue = deque()
    s_queue.append(s)
    e_queue = deque()
    e_queue.append(e)
    while True:
        for node in s_queue:
            if(node in e_queue):
                return (front, s_queue, back, e_queue) 
        u = s_queue.popleft()
        for n in Graph.adj(u, 'front'):
            if n not in front.level:
                front.parent[n] = u
                front.level[n] = front.level[u] + 1
                s_queue.append(n)
        v = e_queue.popleft()
        for m in Graph.adj(v, 'back'):
            if m not in back.level:
                back.parent[m] = v
                back.level[m] = back.level[v] + 1
                e_queue.append(m)
        
        

if __name__ == '__main__':
    start = rubik.I
    middle = rubik.perm_apply(rubik.F, start)
    end = rubik.perm_apply(rubik.Li, middle)
    (front, f_q, back, b_q) = bfs(start, end)
    best_node = find_minimal_d(front, f_q, back, b_q)
    solution  = get_solution_path(front, back, best_node, start, end)
    
