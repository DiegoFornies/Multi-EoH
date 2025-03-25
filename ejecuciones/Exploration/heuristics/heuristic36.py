
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with fewer machine options
    and shorter processing times to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 0))  # (job_id, operation_index)

    while eligible_operations:
        # Prioritize operations with fewer machine choices and shorter processing times
        eligible_operations.sort(key=lambda item: (
            len(jobs_data[item[0]][item[1]][0]),  # Fewer machine options
            min(jobs_data[item[0]][item[1]][1]) if jobs_data[item[0]][item[1]][1] else float('inf') # Shorter processing time
        ))

        job_id, op_idx = eligible_operations.pop(0)
        machines, times = jobs_data[job_id][op_idx]

        # Find the machine that allows the earliest start time for this operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]  # Use the corresponding processing time

        # Schedule the operation on the best machine
        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Add the next operation of this job to eligible operations, if it exists
        if op_idx + 1 < len(jobs_data[job_id]):
            eligible_operations.append((job_id, op_idx + 1))

    return schedule
