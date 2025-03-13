import numpy as np
from collections import defaultdict

def objective_functions(solution):

    def calculate_makespan(solution): #minimize
        makespan = 0
        for job_operations in solution.values():
            for operation in job_operations:
                end_time = operation['End Time']
                makespan = max(makespan, end_time)
        return makespan

    def calculate_operation_separation(solution): #minimize

        total_wait_time = 0

        for job_operations in solution.values():
            job_operations.sort(key=lambda op: op["Operation"])

            for i in range(1, len(job_operations)):
                prev_end = job_operations[i - 1]["End Time"]
                curr_start = job_operations[i]["Start Time"]

                if curr_start > prev_end:
                    total_wait_time += curr_start - prev_end

        return total_wait_time

    def calculate_balance_load(solution): #minimize

        machine_loads = defaultdict(int)

        for job_operations in solution.values():
            for operation in job_operations:
                machine = operation["Assigned Machine"]
                machine_loads[machine] += operation["Processing Time"]

        loads = list(machine_loads.values())

        if len(loads) < 2:
            return 0  

        return np.std(loads)

    return {'Makespan': calculate_makespan(solution), 'Separation': calculate_operation_separation(solution), 'Balance': calculate_balance_load(solution)}