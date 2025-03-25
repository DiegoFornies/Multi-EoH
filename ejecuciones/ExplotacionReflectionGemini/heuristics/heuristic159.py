
def heuristic(input_data):
    """A two-phase heuristic: minimize makespan then balance machine load."""
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
        available_operations.append((job_id, 0))  # (job_id, operation_index)

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')  # Changed to end time

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:  # Prioritize earlier end times
                    earliest_end_time = end_time
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

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Phase 2: Machine Load Balancing (Simple Swap)
    # Iterate through schedule to look for opportunities to balance machine load
    for job_id in schedule:
        for op_idx, operation in enumerate(schedule[job_id]):
            current_machine = operation['Assigned Machine']
            current_start_time = operation['Start Time']
            current_end_time = operation['End Time']
            current_processing_time = operation['Processing Time']
            operation_data = jobs[job_id][op_idx]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Try swapping with a different machine if possible
            for i, possible_machine in enumerate(possible_machines):
                if possible_machine != current_machine:
                    possible_processing_time = possible_times[i]
                    possible_start_time = max(machine_available_time[possible_machine] - current_processing_time + possible_processing_time, job_completion_time[job_id] - current_processing_time + possible_processing_time)
                    possible_end_time = possible_start_time + possible_processing_time

                    # Check feasibility: Ensure the new schedule doesn't violate precedence constraints within the job
                    is_feasible = True
                    if op_idx > 0:
                        if possible_start_time < schedule[job_id][op_idx - 1]['End Time']:
                            is_feasible = False
                    if op_idx < len(schedule[job_id]) - 1:
                         if possible_end_time > machine_available_time[possible_machine]: # Check that processing is possible after previous job on machine
                            is_feasible = False


                    if is_feasible:
                        # Calculate load difference: Check if it improves balance
                        current_load = machine_available_time[current_machine]
                        possible_load = machine_available_time[possible_machine]
                        if current_load > possible_load: # Balance toward the possible machine
                            # Update Schedule
                            operation['Assigned Machine'] = possible_machine
                            operation['Start Time'] = possible_start_time
                            operation['End Time'] = possible_end_time
                            operation['Processing Time'] = possible_processing_time

                            #Update machine times and job completion
                            machine_available_time[current_machine] -= current_processing_time #Reduce time from current machine
                            machine_available_time[possible_machine] = possible_end_time # Increase time to possible machine
                            job_completion_time[job_id] -= current_processing_time
                            job_completion_time[job_id] = possible_end_time #Update Job Complete Time
                            break #Swap made - go to next operation
    return schedule
