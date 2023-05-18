#code to solve 8 puzzle using heapq with three heuristic functions
import heapq
import time
import sys
import copy


#global variables
goal_state = [[1,2,3],[4,5,6],[7,8,0]]
id_counter= 0

#class to store the state of the puzzle
class State:
    def __init__(self, state, heuristic, parent=None,depth=0):
        self.state = state
        self.parent=parent
        self.depth = depth
        self.heuristic=heuristic
        global id_counter
        self.id = id_counter
        id_counter += 1


        if heuristic==1:
            self.cost=self.get_misplaced_tiles_heuristic()+self.depth
        elif heuristic==2:
            self.cost=self.get_manhattan_distance_heuristic()+self.depth
        elif heuristic==3:
            self.cost=self.get_uniform_cost_heuristic()+self.depth
        else:
            print("Invalid heuristic")
            sys.exit()

    #function to return misplace tiles heuristic
    def get_misplaced_tiles_heuristic(self):
        heuristic = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != goal_state[i][j]:
                    heuristic += 1
        return heuristic
    
    #function to return manhattan distance heuristic
    def get_manhattan_distance_heuristic(self):
        heuristic = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    x = (self.state[i][j] - 1) // 3
                    y = (self.state[i][j] - 1) % 3
                    heuristic += abs(x - i) + abs(y - j)
        return heuristic
    
    #function to return uniform cost heuristic
    def get_uniform_cost_heuristic(self):
        return 0
    
    #function to print the state
    def print_state(self):
        for i in range(3):
            for j in range(3):
                print(self.state[i][j], end = " ")
            print()
        print()
    
    #function to check if the state is the goal state
    def is_goal_state(self):
        if self.state == goal_state:
            return True
        return False
    
    #function to check if the state is valid
    def is_valid_state(self):
        if len(self.state) == 3 and len(self.state[0]) == 3 and len(self.state[1]) == 3 and len(self.state[2]) == 3:
            return True
        return False
    
    
    #function to return the list of child states
    def get_children(self):
        children = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    if i > 0:
                        child = copy.deepcopy(self.state)
                        child[i][j] = child[i - 1][j]
                        child[i - 1][j] = 0
                        children.append(child)
                    if i < 2:
                        child = copy.deepcopy(self.state)
                        child[i][j] = child[i + 1][j]
                        child[i + 1][j] = 0
                        children.append(child)
                    if j > 0:
                        child = copy.deepcopy(self.state)
                        child[i][j] = child[i][j - 1]
                        child[i][j - 1] = 0
                        children.append(child)
                    if j < 2:
                        child = copy.deepcopy(self.state)
                        child[i][j] = child[i][j + 1]
                        child[i][j + 1] = 0
                        children.append(child)

        child_nodes = []              
        for i in children:
            child_nodes.append(State(i, self.heuristic, self, self.depth + 1))
        return child_nodes

    
    
    
    
    #function to return the path from the initial state to the current state
    def get_path(self):
        path = []
        state = self
        while state != None:
            path.append(state)
            state = state.parent
        path.reverse()
        return path
    

#function to solve the puzzle using A* and uniform cost search
def solve_puzzle(initial_state, heuristic):
    initial_state=State(initial_state,heuristic)
    if not initial_state.is_valid_state():
        print("Invalid initial state")
        return
    if initial_state.is_goal_state():
        print("Initial state is the goal state")
        return [0, 0, 0]
    if heuristic == 1:
        print("Using misplaced tiles heuristic")
    elif heuristic == 2:
        print("Using manhattan distance heuristic")
    elif heuristic == 3:
        print("Using uniform cost heuristic")
    else:
        print("Invalid heuristic")
        return
    
    print("Initial state:")
    initial_state.print_state()
    start_time = time.time()
    visited = set()
    queue = []
    # to trank max queue size
    max_queue_size = 0
    heapq.heappush(queue, (initial_state.cost, initial_state.id, initial_state))

    while queue:
        state = heapq.heappop(queue)[2]
        if state.is_goal_state():
            print("Goal state reached")
            print("Time taken:", time.time() - start_time)
            print("Number of Nodes Expanded:", len(visited))
            print("Solution depth:", state.depth)
            print("Max queue size:", max_queue_size)
            print("Path:")
            path = state.get_path()
            for state in path:
                print("Move", state.depth)
                state.print_state()
            return [len(visited), max_queue_size, time.time() - start_time]
        if str(state.state) in visited:
            continue
        visited.add(str(state.state))
        next_states = state.get_children()
        for next_state in next_states:
            if str(next_state) in visited:
                continue
            heapq.heappush(queue, (next_state.cost, next_state.id, next_state))
        if len(queue) > max_queue_size:
            max_queue_size = len(queue)
    print("Goal state not reachable")
    print("Time taken:", time.time() - start_time)
    print("Number of Nodes Expanded:", len(visited))
    return


if __name__ == "__main__":
    print("Welcome to 8-puzzle solver")
    print("Do you want to use any state from default states(0) or enter your own puzzle(1)?")
    choice = int(input())
    if choice == 0:
        print("Enter the initial state to be used:")
        print("1. Default state 1 with solution depth 0")
        print("[[1, 2, 3],\n [4, 5, 6],\n [7, 8, 0]]")
        print("2. Default state 2 with solution depth 2")
        print("[[1, 2, 3],\n [4, 5, 6],\n [0, 7, 8]]")
        print("3. Default state 3 with solution depth 4")
        print("[[1, 2, 3],\n [5, 0, 6],\n [4, 7, 8]]")
        print("4. Default state 4 with solution depth 8")
        print("[[1, 3, 6],\n [5, 0, 2],\n [4, 7, 8]]")
        print("5. Default state 5 with solution depth 12")
        print("[[1, 3, 6],\n [5, 0, 7],\n [4, 8, 2]]")
        print("6. Default state 6 with solution depth 16")
        print("[[1, 6, 7],\n [5, 0, 3],\n [4, 8, 2]]")
        print("7. Default state 7 with solution depth 20")
        print("[[7, 1, 2],\n [4, 8, 5],\n [6, 3, 0]]")
        print("8. Default state 8 with solution depth 24")
        print("[[0, 7, 2],\n [4, 6, 1],\n [3, 5, 8]]")

        state_choice = int(input())
        if state_choice == 1:
            initial_state = [[1, 2, 3],
                             [4, 5, 6], 
                             [7, 8, 0]]
        elif state_choice == 2:
            initial_state = [[1, 2, 3],
                             [4, 5, 6], 
                             [0, 7, 8]]
        elif state_choice == 3:
            initial_state = [[1, 2, 3],
                             [5, 0, 6],
                             [4, 7, 8]]
        elif state_choice == 4:
            initial_state = [[1, 3, 6],
                             [5, 0, 2],
                             [4, 7, 8]]
        elif state_choice == 5:
            initial_state = [[1, 3, 6],
                             [5, 0, 7],
                             [4, 8, 2]]
        elif state_choice == 6:
            initial_state = [[1, 6, 7],
                             [5, 0, 3],
                             [4, 8, 2]]
        elif state_choice == 7:
            initial_state = [[7, 1, 2],
                             [4, 8, 5],
                             [6, 3, 0]]
        elif state_choice == 8:
            initial_state = [[0, 7, 2],
                             [4, 6, 1],
                             [3, 5, 8]]
        else:
            print("Invalid choice")
            exit()
    #Take input from the user
    else:
        print("Enter the initial state:")
        initial_state = []
        for i in range(3):
            initial_state.append(list(map(int, input().split())))
    print("Choose the heuristic type from below:")
    print("1. Misplaced tiles heuristic")
    print("2. Manhattan distance heuristic")
    print("3. Uniform cost Search")
    heuristic = int(input())
    solve_puzzle(initial_state, heuristic)




