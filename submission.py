from mars_planner import RoverState, start_state_subproblem_1, action_list, moveToSample, start_state_subproblem_2, \
    removeSample, start_state_subproblem_3, mission_complete
from routefinder import a_star, read_mars_graph, map_state, ucs, h1, sld
from search_algorithms import breadth_first_search, depth_first_search, depth_limited_search


## Main execution
if __name__=="__main__" :
    s = RoverState()
    limit = 15 # set desired limit for DLS

    ## BFS
    # Subproblem 1: Moving to the sample
    print("Subproblem 1: Moving to the sample")
    s1 = start_state_subproblem_1()
    BFSresult_1 = breadth_first_search(s1, action_list, moveToSample)
    print(f"BFS Result: {BFSresult_1}")

    # Subproblem 2: Collecting the sample
    print("\nSubproblem 2: Collecting the sample")
    s2 = start_state_subproblem_2()
    BFSresult_2 = breadth_first_search(s2, action_list, removeSample)
    print(f"BFS Result: {BFSresult_2}")

    # Subproblem 3: Returning to the station and charging
    print("\nSubproblem 3: Returning to the station and charging")
    s3 = start_state_subproblem_3()
    BFSresult_3 = breadth_first_search(s3, action_list, mission_complete)
    print(f"BFS Result: {BFSresult_3}")

    ## DFS
    # Subproblem 1: Moving to the sample
    print("Subproblem 1: Moving to the sample")
    s1 = start_state_subproblem_1()
    DFSresult_1 = depth_first_search(s1, action_list, moveToSample)
    print(f"DFS Result: {DFSresult_1}")

    # Subproblem 2: Collecting the sample
    print("\nSubproblem 2: Collecting the sample")
    s2 = start_state_subproblem_2()
    DFSresult_2 = depth_first_search(s2, action_list, removeSample)
    print(f"DFS Result: {DFSresult_2}")

    # Subproblem 3: Returning to the station and charging
    print("\nSubproblem 3: Returning to the station and charging")
    s3 = start_state_subproblem_3()
    DFSresult_3 = depth_first_search(s3, action_list, mission_complete)
    print(f"DFS Result: {DFSresult_3}")

    ## DLS
    # Subproblem 1: Moving to the sample
    print("Subproblem 1: Moving to the sample")
    s1 = start_state_subproblem_1()
    DLSresult_1 = depth_limited_search(s1, action_list, moveToSample, limit)
    print(f"DLS Result: {DLSresult_1}")

    # Subproblem 2: Collecting the sample
    print("\nSubproblem 2: Collecting the sample")
    s2 = start_state_subproblem_2()
    DLSresult_2 = depth_limited_search(s2, action_list, removeSample, limit)
    print(f"DLS Result: {DLSresult_2}")

    # Subproblem 3: Returning to the station and charging
    print("\nSubproblem 3: Returning to the station and charging")
    s3 = start_state_subproblem_3()
    DLSresult_3 = depth_limited_search(s3, action_list, mission_complete, limit)
    print(f"DLS Result: {DLSresult_3}")


    ## A* and UCS
    print("\nRunning A* and UCS...")
    mars_graph = read_mars_graph('MarsMap.txt')
    start_state = map_state(location='8,8', mars_graph=mars_graph)
    goal_test = lambda state: state.is_goal()

    a_star_path, a_star_states_generated = a_star(start_state, sld, lambda state: state.is_goal())
    print(f"A* Path: {a_star_path}, \nStates Generated: {a_star_states_generated}")

    ucs_path, ucs_states_generated = ucs(start_state, h1, lambda state: state.is_goal())
    print(f"UCS Path: {ucs_path}, \nStates Generated: {ucs_states_generated}")
