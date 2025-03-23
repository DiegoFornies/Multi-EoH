
def heuristic(input_data):
    """
    A heuristic algorithm for FJSSP.
    It prioritizes operations with fewer machine options and shorter processing times,
    dynamically selecting machines to minimize idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 0))  # (job_id, operation_index)

    while eligible_operations:
        # Prioritize operations based on machine choice count and processing time
        eligible_operations.sort(key=lambda x: (len(jobs_data[x[0]][x[1]][0]),
                                                  min(jobs_data[x[0]][x[1]][1])))

        job_id, operation_index = eligible_operations.pop(0)
        machines, times = jobs_data[job_id][operation_index]

        # Find the best machine and start time for this operation
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m, t in zip(machines, times):
            start_time = max(machine_available_times[m], job_completion_times[job_id])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = t

        # Schedule the operation
        start_time = best_start_time
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Add the next operation of the job to the eligible operations
        if operation_index + 1 < len(jobs_data[job_id]):
            eligible_operations.append((job_id, operation_index + 1))
            

    return schedule
