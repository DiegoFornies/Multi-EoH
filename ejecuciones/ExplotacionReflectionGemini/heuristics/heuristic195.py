
def heuristic(input_data):
    """Hybrid heuristic: Minimizes makespan then reduces idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Phase 1: Makespan Minimization (Greedy)
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        available_operations.remove((job_id, op_idx))

        # Add the next operation
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Phase 2: Idle Time Reduction
    for job_id in range(1, n_jobs + 1):
        if len(schedule[job_id]) > 1:
            for i in range(len(schedule[job_id]) - 1):
                current_end_time = schedule[job_id][i]['End Time']
                next_start_time = schedule[job_id][i+1]['Start Time']
                idle_time = next_start_time - current_end_time

                if idle_time > 0:
                    # Try shifting the next operation to reduce idle time
                    machines = jobs[job_id][i+1][0]
                    original_machine = schedule[job_id][i+1]['Assigned Machine']
                    original_processing_time = schedule[job_id][i+1]['Processing Time']

                    for alt_machine_idx, alt_machine in enumerate(machines):
                        if alt_machine != original_machine:
                            alt_processing_time = jobs[job_id][i+1][1][alt_machine_idx]
                            potential_start_time = max(machine_available_time[alt_machine], current_end_time)
                            potential_end_time = potential_start_time + alt_processing_time
                            
                            if potential_start_time < next_start_time:
                                schedule[job_id][i+1]['Assigned Machine'] = alt_machine
                                schedule[job_id][i+1]['Start Time'] = potential_start_time
                                schedule[job_id][i+1]['End Time'] = potential_end_time
                                schedule[job_id][i+1]['Processing Time'] = alt_processing_time
                                
                                machine_available_time[alt_machine] = potential_end_time
                                
                                # Correct subsequent operation times in current job
                                for k in range(i+2, len(schedule[job_id])):
                                    prev_end_time = schedule[job_id][k-1]['End Time']
                                    machine = schedule[job_id][k]['Assigned Machine']
                                    schedule[job_id][k]['Start Time'] = max(machine_available_time[machine], prev_end_time)
                                    schedule[job_id][k]['End Time'] = schedule[job_id][k]['Start Time'] + schedule[job_id][k]['Processing Time']

    return schedule
