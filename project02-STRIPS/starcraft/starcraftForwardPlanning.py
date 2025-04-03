import time
import pandas as pd

from library.searchMPP import SearcherMPP
from starcraft.starcraftProblem import *
from library.stripsForwardPlanner import Forward_STRIPS

#heuristics
def h_minerals(state, goal):
    return 10 if not state['scv_has_minerals'] else 0

def h_building_needed(state, goal):

    buildings = ['supply_depot', 'barracks', 'factory', 'starport', 'fusion_core']
    units = ['marine', 'tank', 'wraith', 'battlecruiser']

    highest = max(max((idx for idx, building in enumerate(buildings) if facility_is_built(building) in goal), default=0),
                  max((idx for idx, unit in enumerate(units) if is_unit_trained(unit) in goal), default=0) + 1)

    buildings_needed = buildings[0:highest]

    missing_buildings = sum(1 for building in buildings_needed if state[facility_is_built(building)] is None)

    return missing_buildings * 2


def h_combined(state, goal):
    return max(h_minerals(state, goal), h_building_needed(state, goal))

#tests

def get_time(forward_strips):
    start_time = time.perf_counter()
    SearcherMPP(forward_strips).search()
    stop_time = time.perf_counter()
    elapsed_time = stop_time - start_time
    return elapsed_time

def run_with_stats(tasks):

    df = pd.DataFrame(columns=['Problem name','Execution time(s) without heuristic','Execution time(s) with heuristic'])

    for name, task in tasks.items():
        time_without = get_time(Forward_STRIPS(task))
        time_with = get_time(Forward_STRIPS(task, h_combined))

        new_row = pd.DataFrame([{'Problem name': name,
                                 'Execution time(s) without heuristic': time_without,
                                 'Execution time(s) with heuristic': time_with}])

        df = pd.concat([df, new_row], ignore_index=True)

    return df

#run_with_stats({'train marine' : problem_train_marine})

# results = run_with_stats(problems)
# results.to_csv('results1.csv')

def run_with_subgoals(problems_list):

    results = []

    for prob in problems_list:
        name = prob["name"]
        domain = prob["domain"]
        initial_state = prob["initial_state"]
        subgoals = prob["subgoals"]

        # RUN WITHOUT HEURISTIC
        # state_no_heur = initial_state
        # start_time = time.time()
        # for goal in subgoals:
        #     problem = Planning_problem(domain, state_no_heur, goal)
        #     result = SearcherMPP(Forward_STRIPS(problem)).search()
        #     if result is None:
        #         print(f"[NO HEUR] No solution for subgoal: {goal}")
        #         break
        #     state_no_heur = result.end().assignment
        # end_time = time.time()
        # time_no_heur = end_time - start_time

        # RUN WITH HEURISTIC
        state_heur = initial_state
        start_time = time.time()
        for goal in subgoals:
            problem = Planning_problem(domain, state_heur, goal)
            result = SearcherMPP(Forward_STRIPS(problem, h_combined)).search()
            if result is None:
                print(f"[HEUR] No solution for subgoal: {goal}")
                break
            state_heur = result.end().assignment
        end_time = time.time()
        time_with_heur = end_time - start_time

        # ADD TO RESULTS
        results.append({
            "Problem": name,
            # "Time_no_heuristic": time_no_heur,
            "Time_with_heuristic": time_with_heur
        })

    df = pd.DataFrame(results)
    return df

# results4 = run_with_subgoals(problems_with_subgoals)
# results4.to_csv('results4.csv')

results5 = run_with_subgoals(hard_problems_with_subgoals)
results5.to_csv('results5.csv')

