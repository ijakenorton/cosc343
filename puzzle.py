from cosc343EightPuzzle import EightPuzzle
import time
import itertools

class Node:
    
    def __init__(self, s ,parent=None, g=0,h=0, action=None) -> None:
        self.s = s
        self.parent = parent
        self.g = g
        self.f = g+h
        self.action = action

def heuristic(s,goal):
    h = 0
    for i in range(len(s)):
        if s[i] != goal[i]:

            current = abs((i // 3 ) - (s[i] // 3)) + abs((i % 3) - (s[i] % 3))
            h += current
            # print("s " ,s[i], "goal ", current_index, current )
            
    return h 

# def heuristic(s,goal):
#     h = 0
#     for i in range(len(s)):
#         print("s " ,s[i], "goal ", goal[i])
#         if s[i] != goal[i]:
            
#             h+=1
#     return h 
def solve(state):
    print(state)
    start_time = time.time()
    puzzle = EightPuzzle(mode='hard', state=state)

    goal_state = puzzle.goal()

    init_state = puzzle.reset()

    root_node = Node(s=init_state, parent=None, g=0, h=heuristic(s=init_state, goal = goal_state))

    fringe = [root_node]

    solution_node = None
    seen = list()
    while len(fringe)>0:
        current_node = fringe.pop(0)
        current_state = current_node.s
        seen.append(current_state)
        if current_state == goal_state:
            solution_node = current_node
            break
        else:
            available_actions = puzzle.actions(s=current_state)
            for a in available_actions:
                print(a)
                next_state = puzzle.step(s=current_state, a=a)
                new_node = Node(s=next_state, parent=current_node, g = current_node.g+1, h=heuristic(s=next_state, goal=goal_state),
                                action=a)
                if not new_node.s in seen:
                    fringe.append(new_node)
            fringe.sort(key=lambda x:x.f)
            
    if solution_node is None:
        print("Didn't find a solution")
    else:
        action_sequence = []
        next_node = solution_node
        while True:
            if next_node == root_node:
                break
            
            action_sequence.append(next_node.action)
            next_node = next_node.parent
        
        action_sequence.reverse()
        print("Number of moves: ", solution_node.g)
    elapsed_time = time.time() - start_time
    print("Time: %.1f seconds" % elapsed_time)
    # puzzle.show(s=init_state, a=action_sequence)
    
def main():
    default = [0,1,2,3,4,5,6,7,8]
    permutations_object = itertools.permutations(default)
    permutations_list = list(permutations_object)
    # for perm in permutations_list:
    #     print(list(perm))
    for puzzle in permutations_list:
        solve(puzzle)
    
if __name__ == "__main__":
    main()