from queue import PriorityQueue
import math

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'

# Graph object
class Graph:
    def __init__(self):
        # Adjacency list to store the graph
        self.adjacency_list = {}

    def add_edge(self, node, neighbors):
        # Add neighbors for a node
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
        self.adjacency_list[node].extend(neighbors)

    def get_neighbors(self, node):
        # Return neighbors of the node
        return self.adjacency_list.get(node, [])

    def __repr__(self):
        return str(self.adjacency_list)

## Uses sld as heuristic
def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True):
    search_queue = PriorityQueue()
    closed_list = {}  # To store the best g values for each location
    states_generated = 0  # Counter for generated states

    # Add the start state to the queue
    search_queue.put((start_state.f, start_state))  # (f, state) - priority queue uses f
    states_generated += 1  # Increment counter when the start state is added

    while not search_queue.empty():
        # Get the state with the lowest f value
        current_f, current_state = search_queue.get()

        # Check if the current state is the goal
        if goal_test(current_state):
            # Reconstruct path (by backtracking through prev_state)
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1], states_generated  # Return the path from start to goal and the number of states generated

        # If using closed list, add the current state to it
        if use_closed_list:
            closed_list[current_state.location] = current_state.g

        # Expand neighbors
        for neighbor in current_state.mars_graph.get_neighbors(current_state.location):
            # Create a new state for the neighbor
            g_cost = current_state.g + 1  # Assuming all moves have a cost of 1
            h_cost = heuristic_fn(map_state(location=neighbor))  # Heuristic from neighbor to goal
            neighbor_state = map_state(location=neighbor, mars_graph=current_state.mars_graph,
                                       prev_state=current_state, g=g_cost, h=h_cost)

            # If using closed list, skip if this state has already been explored with a lower g
            if use_closed_list and neighbor_state.location in closed_list and g_cost >= closed_list[
                neighbor_state.location]:
                continue

            # Add the neighbor to the search queue
            search_queue.put((neighbor_state.f, neighbor_state))
            states_generated += 1  # Increment counter when a neighbor state is added

    # If the search queue is empty and no goal found
    return None, states_generated


## Uses h1 as heuristic_fn (for UCS)
def ucs(start_state, heuristic_fn, goal_test, use_closed_list=True):
    search_queue = PriorityQueue()
    closed_list = {}  # To store the best g values for each location
    state_counter = 0  # Counter for generated states

    # Add the start state to the queue
    search_queue.put((start_state.f, start_state))  # (f, state) - priority queue uses f
    state_counter += 1  # Increment counter when the start state is added

    while not search_queue.empty():
        # Get the state with the lowest f value
        current_f, current_state = search_queue.get()

        # Check if the current state is the goal
        if goal_test(current_state):
            # Reconstruct path (by backtracking through prev_state)
            path = []
            while current_state:
                path.append(current_state)
                current_state = current_state.prev_state
            return path[::-1], state_counter  # Return the path from start to goal and the number of states generated

        # If using closed list, add the current state to it
        if use_closed_list:
            closed_list[current_state.location] = current_state.g

        # Expand neighbors
        for neighbor in current_state.mars_graph.get_neighbors(current_state.location):
            # Create a new state for the neighbor
            g_cost = current_state.g + 1  # Assuming all moves have a cost of 1
            h_cost = heuristic_fn(map_state(location=neighbor))  # Heuristic from neighbor to goal
            neighbor_state = map_state(location=neighbor, mars_graph=current_state.mars_graph,
                                       prev_state=current_state, g=g_cost, h=h_cost)

            # If using closed list, skip if this state has already been explored with a lower g
            if use_closed_list and neighbor_state.location in closed_list and g_cost >= closed_list[
                neighbor_state.location]:
                continue

            # Add the neighbor to the search queue
            search_queue.put((neighbor_state.f, neighbor_state))
            state_counter += 1  # Increment counter when a neighbor state is added

    # If the search queue is empty and no goal found
    return None, state_counter


## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state):
    # Parse the current state's location
    x1, y1 = map(int, state.location.split(','))  # Convert 'x,y' string to integers
    # Goal location is fixed at (1,1)
    x2, y2 = 1, 1
    # Compute the straight-line distance using the Euclidean distance formula
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    mars_graph = Graph()  # Create a Graph object

    with open(filename, 'r') as file:
        for line in file:
            # Split the line at ": " to separate the node from its neighbors
            location, neighbors = line.strip().split(": ")
            neighbors_list = neighbors.split(" ")

            # Add the node and its neighbors to the graph
            mars_graph.add_edge(location, neighbors_list)

    return mars_graph
