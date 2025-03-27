
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing machine idle time
    and balances workload across machines, with some level of randomness.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_assignments = {m: [] for m in range(n_machines)} # jobs assigned to each machine

    import random

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            # Heuristic 1: Find the machine with earliest available time among feasible machine
            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, current_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id

            #Heuristic 2: Tie-breaking: Prefer machine with fewer jobs
            contenders = []
            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, current_time)
                end_time = start_time + processing_time

                if end_time == min_end_time:
                  contenders.append(machine_id)
            
            if len(contenders) > 1:
              best_machine = min(contenders, key = lambda m: len(machine_assignments[m]))


            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            machine_assignments[best_machine].append(job_id)
            current_time = end_time

    return schedule
