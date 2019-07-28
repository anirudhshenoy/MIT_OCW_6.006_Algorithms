import rubik
from collections import deque


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 
    Assumes the rubik.quarter_twists move set.
    """
    (front, f_q, back, b_q) = bfs(start, end)
    best_node = find_minimal_d(front, back)
    solution  = get_solution_path(front, back, best_node, start, end)
    return solution 


class Graph:
    @staticmethod
    def adj(u, dir):
        adj_u = []
        for move in rubik.quarter_twists:
            if(dir):
                adj_u.append(rubik.perm_apply(move, u))
            else:
                adj_u.append(rubik.perm_apply(rubik.perm_inverse(move), u))
        return adj_u


class BFSResult:
    def __init__(self):
        self.level = {}
        self.parent = {}


def find_minimal_d(front, back):
    smallest = float("inf") 
    for node in front.keys():
        if(node in back.keys()):
            print "hello"
            temp = front.get(node) + back.get(node)  
            if(temp < smallest):
                smallest = temp
                best_node = node
    return best_node       
    
def get_solution_path(front, back, best_node, s, end):
    solution_front = []
    solution_back =[] 
    FORWARD = 1
    BACKWARD = 0
    v = best_node
    print("Front Moves: ")
    while(v!=s):
        solution_front.append(front[v][0])
        v = front[v][1]
    solution_front.reverse()
    for move in solution_front: 
       print(rubik.quarter_twists_names[move])
    v = best_node
    while(v!=end):
        solution_back.append(back[v][0])
        v = back[v][1]
    print("Back Moves:")
    for move in solution_back: 
        print(rubik.quarter_twists_names[move])
    solution = solution_front + solution_back
    #print(solution)
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
    front_parents = {s: None}
    back_parents = {e: None} 
    # front_moves = rubik.quarter_twists
    #back_moves = (rubik.perm_inverse(move) for move in rubik.quarter_twists)
    front_moves={}
    back_moves = {}
    for move in rubik.quarter_twists:
        front_moves[move] = move
        back_moves[rubik.perm_inverse(move)] = move
    front = (front_moves, front_parents, back_parents)
    back = (back_moves, back_parents, front_parents)
    queue = deque([(s, front), (e, back), None])

    for i in range(7):
        while True:
            node = queue.popleft()
            if node is None: # One Level of BFS complete
                queue.append(None)
                break
            current_node = node[0]
            moves, parents, other_parents = node[1]
            for move in moves:
                next_node = rubik.perm_apply(move, current_node)
                if next_node in parents: continue
                parents[next_node] = (moves[move], current_node)
                queue.append((next_node, node[1]))
                if next_node in other_parents:
                    return (front_parents, back_parents, next_node)


    return None









    """
    Spaghetti Code:

    front = BFSResult()
    front.parent = {s: None}
    front.level = {s: 0}
    back = BFSResult()
    back.parent = {e: None}
    back.level = {e: 0}
    s_queue = deque([s, None])
    e_queue = deque([e, None])
    while True:
        u = s_queue.popleft()
        if u is None:
            queue.append(None)
            break
        for n in Graph.adj(u, 1):
            if n not in front.level:
                front.parent[n] = u
                front.level[n] = front.level[u] + 1
                s_queue.append(n)
                if n in back.level:
                   return (front, s_queue, back, e_queue)  
        v = e_queue.popleft()
        for m in Graph.adj(v, 0):
            if m not in back.level:
                back.parent[m] = v
                back.level[m] = back.level[v] + 1
                e_queue.append(m)
                if m in front.level:
                    return (front, s_queue, back, e_queue) 

    """    
        

if __name__ == '__main__':
    #start = rubik.I
    start = (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
    #middle = rubik.perm_apply(rubik.F, start)
    #middle2 = rubik.perm_apply(rubik.L, middle)
    #middle3 = rubik.perm_apply(rubik.F, middle2)
    #middle4 = rubik.perm_apply(rubik.Li,middle3)
    #for i in (rubik.F, rubik.U, rubik.L, rubik.F, rubik.Ui):
    #    middle = rubik.perm_apply(i, middle)
    #end = rubik.perm_apply(rubik.L, middle)
    end = rubik.I
    (front, back, best_node) = bfs(start, end)
    solution  = get_solution_path(front, back, best_node, start, end)
    print(solution)
     
