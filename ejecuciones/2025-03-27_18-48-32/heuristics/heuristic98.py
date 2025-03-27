
def heuristic(input_data):
    """FJSSP heuristic: Hybrid of min start time and adaptive load balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_start_time = float('inf')

            # Heuristic 1: Find machine with earliest possible start time.
            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine_id], current_time)
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine_id

            # Heuristic 2: Adaptive load balancing: if any machine load exceeds the average,
            # select the least loaded machine among possible machines.
            avg_load = sum(machine_load.values()) / n_machines if n_machines > 0 else 0
            overloaded = any(machine_load[m] > avg_load for m in range(n_machines))

            if overloaded:
                least_loaded_machines = [m for m in possible_machines if machine_load[m] <= avg_load]
                if least_loaded_machines:
                    #If multiple available, use the original criteria
                    if len(least_loaded_machines) > 1:
                        min_start_time_tiebreak = float('inf')
                        best_machine = None
                        for i, machine_id in enumerate(least_loaded_machines):
                            processing_time = possible_times[possible_machines.index(machine_id)]
                            start_time = max(machine_available_times[machine_id], current_time)
                            if start_time < min_start_time_tiebreak:
                                min_start_time_tiebreak = start_time
                                best_machine = machine_id
                    else:
                        best_machine = least_loaded_machines[0]

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
            machine_load[best_machine] += processing_time
            current_time = end_time

    return schedule
