from collections import deque
import math
from queue import PriorityQueue

## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    search_queue = deque()
    closed_list = {}
    state_counter = 0 # Initialize state counter

    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            print(f"BFS - Total number of states generated: {state_counter}")  # Print the counter
            return next_state
        else :
            successors = next_state[0].successors(action_list)
            state_counter += len(successors) # Increment counter by number of successors generated
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)

    print(f"BFS - Total number of states generated: {state_counter}")  # Print the counter if no solution is found

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True,limit=0) :
    search_queue = deque()
    closed_list = {}
    state_counter = 0  # Initialize state counter

    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.pop()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            print(f"DFS - Total number of states generated: {state_counter}")  # Print the counter
            return next_state
        else :
            successors = next_state[0].successors(action_list)
            state_counter += len(successors)  # Increment counter by number of successors generated
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)

    print(f"DFS - Total number of states generated: {state_counter}")  # Print the counter if no solution is found

## add iterative deepening search here
def depth_limited_search(startState, action_list, goal_test, limit=0, use_closed_list=True):
    search_queue = deque()
    closed_list = {}
    state_counter = 0  # Initialize the state counter

    # Add (state, action, depth) to the search queue
    search_queue.append((startState, "", 0))
    if use_closed_list:
        closed_list[startState] = True

    while len(search_queue) > 0:
        # Pop (state, action, depth) from the search queue
        next_state, action, depth = search_queue.pop()

        # If we exceed the limit, don't generate further successors
        if depth >= limit:
            continue

        # Check if the current state is the goal
        if goal_test(next_state):
            print("Goal found")
            print((next_state, action))
            ptr = next_state
            while ptr is not None:
                ptr = ptr.prev
                print(ptr)
            print(f"DLS - Total number of states generated: {state_counter}")  # Print the counter
            return (next_state, action)

        else:
            # Generate successors only if we are within the depth limit
            successors = next_state.successors(action_list)
            state_counter += len(successors)  # Increment counter by number of successors generated
            if use_closed_list:
                successors = [item for item in successors if item[0] not in closed_list]
                for s in successors:
                    closed_list[s[0]] = True

            # Add successors to the stack with incremented depth
            search_queue.extend([(s[0], s[1], depth + 1) for s in successors])

    # Print the counter if no solution is found
    print(f"DLS - Total number of states generated: {state_counter}")