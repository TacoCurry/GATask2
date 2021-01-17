from Output import *
from Solution import Solution
from Input import *
import math
import random
import copy
import time


def run():
    # Input from files
    processor, memories, ga_configs = get_configuration()
    Solution.processor, Solution.memories, Solution.ga_configs = processor, memories, ga_configs
    Solution.rt_tasks = get_rt_tasks()

    # Initiate out.txt
    init_out()

    crossover_rate = 0.8

    # Get total utils
    original_utils = sum([task.wcet / task.period for task in Solution.rt_tasks])
    print("Original Total util: {}".format(original_utils))

    start_time = time.time()

    for core_max in range(Solution.processor.n_core, math.ceil(original_utils) - 1, -1):
        # 1. Make initial solution set
        Solution.set_random_seed()
        solutions = [Solution.get_random_solution(core_max)
                     for _ in range(ga_configs.POPULATIONS)]
        solutions.sort()  # Sort solutions by score

        for g in range(ga_configs.MAX_GEN):
            # if g != 0 and g % 2 == 0:
            report_print(core_max, g, solutions, start_time)

            new_solutions = []
            for try_count in range(ga_configs.TRY_LIMIT):
                # 2. 엘리트 10개 골라서 그대로 넣는다
                for solution in solutions[:10]:
                    new_solutions.append(copy.deepcopy(solution))

                # 3. (Select two solution and Crossover and Mutation and Check Validity) * 90
                for _ in range(90):
                    if random.uniform(0, 1) <= crossover_rate:  # 크로스오버 O
                        # 3.1.1 Select two solution
                        solution1_index, solution1 = Solution.select_solution_using_roulette_wheel(solutions)
                        solution2_index, solution2 = Solution.select_solution_using_roulette_wheel(solutions)
                        solutions.insert(solution2_index, solution2)
                        solutions.insert(solution1_index, solution1)

                        # 3.1.2 Crossover & Mutation
                        new_solution = Solution.crossover(solution1, solution2)
                        new_solution.mutation()

                        new_solutions.append(new_solution)

                    else:  # 크로스오버 X
                        solution1_index, solution1 = Solution.select_solution_using_roulette_wheel(solutions)
                        solutions.insert(solution1_index, solution1)

                        new_solution = copy.deepcopy(solution1)
                        new_solution.mutation()
                        new_solutions.append(new_solution)

                get_new_solutions = True
                # 4. check Validity
                for solution in new_solutions:
                    solution.calc_memory_used()
                    solution.calc_memory_with_most_tasks()
                    if not solution.check_memory() or not solution.check_utilization(core_max):
                        get_new_solutions = False
                        break

                if not get_new_solutions:
                    if try_count < ga_configs.TRY_LIMIT - 1:
                        continue
                    else:
                        raise Exception("{}th generation 이후로 교배 불가".format(g+1))

                solutions = new_solutions
                solutions.sort()
                break

        # 5. Print result
        for solution in solutions:
            if solution.is_schedule():
                print("n_core: {}".format(core_max))
                print("power: {}, utilization: {}".format(solution.power, solution.utilization))
                result_print(core_max, solution)
                break


run()
