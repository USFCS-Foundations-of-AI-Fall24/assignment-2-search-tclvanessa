from copy import deepcopy
from symbol import and_expr

from search_algorithms import breadth_first_search, depth_first_search, depth_limited_search

## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## pick_up_sample
## drop_sample
## move_to_battery
## charge

class RoverState:
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, charged=False, holding_tool=False, dropped_off_sample=False):
        self.loc = loc
        self.sample_extracted = sample_extracted
        self.holding_sample = holding_sample
        self.charged = charged
        self.holding_tool = holding_tool
        self.dropped_off_sample = dropped_off_sample
        self.prev = None

    def __eq__(self, other):
        return ((self.loc == other.loc and
                 self.sample_extracted == other.sample_extracted and
                 self.holding_sample == other.holding_sample and
                 self.charged == other.charged and
                 self.holding_tool == other.holding_tool and
                 self.dropped_off_sample == other.dropped_off_sample))

    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n" +
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Charged? {self.charged}\n" +
                f"Holding Tool?: {self.holding_tool}\n" +
                f"Dropped Off Sample?: {self.dropped_off_sample}\n")

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions):
        # Apply each function in the list of actions to the current state to get a new state.
        succ = [(item(self), item.__name__) for item in list_of_actions]
        # Remove actions that have no effect
        succ = [item for item in succ if not item[0] == self]
        return succ

## Rover action functions

def move_to_sample(state):
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev = state
    return r2

def move_to_station(state):
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2

def move_to_battery(state):
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2

def pick_up_tool(state):
    r2 = deepcopy(state)
    if state.loc == "station":
        r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state):
    r2 = deepcopy(state)
    if state.loc == "station" and state.sample_extracted:
        r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state):
    r2 = deepcopy(state)
    if state.loc == "sample" and state.holding_tool:
        r2.sample_extracted = True
    r2.prev = state
    return r2

def pick_up_sample(state):
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample":
        r2.holding_sample = True
    r2.prev = state
    return r2

def drop_sample(state):
    r2 = deepcopy(state)
    if state.holding_sample and state.loc == "station":
        r2.holding_sample = False
        r2.dropped_off_sample = True
    r2.prev = state
    return r2

def charge(state):
    r2 = deepcopy(state)
    if state.loc == "battery" and not state.holding_sample:
        r2.charged = True
    r2.prev = state
    return r2

## List of actions
action_list = [charge, drop_sample, pick_up_sample,
               move_to_sample, move_to_battery, move_to_station,
               pick_up_tool, drop_tool, use_tool]

## Also returnToCharger*
def mission_complete(state):
    return (state.sample_extracted and
            state.dropped_off_sample and
            not state.holding_sample and
            state.loc == "battery" and
            state.charged and
            not state.holding_tool)

## Define start states for subproblems
def start_state_subproblem_1():
    return RoverState(loc="station", sample_extracted=False, holding_sample=False, charged=False, holding_tool=False)

def start_state_subproblem_2():
    return RoverState(loc="sample", sample_extracted=False, holding_sample=False, charged=False, holding_tool=True)

def start_state_subproblem_3():
    return RoverState(loc="sample", sample_extracted=True, holding_sample=True, charged=False, holding_tool=True)

## Define goal conditions for subproblems
def moveToSample(state):
    return state.loc == "sample" and state.holding_tool

def removeSample(state):
    return state.sample_extracted and state.holding_sample and state.holding_tool
