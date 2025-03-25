
def heuristic(input_data):
    """Aims to minimize makespan by prioritizing operations based on shortest processing time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of ready operations (operations whose predecessors are completed)
    ready_operations = []
    for job_id, operations in jobs.items():
        ready_operations.append((job_id, 0))  # (job_id, operation_index)

    while ready_operations:
        # Prioritize ready operations based on shortest processing time
        ready_operations.sort(key=lambda x: min(jobs[x[0]][x[1]][1]))  # Sort by min processing time

        job_id, operation_index = ready_operations.pop(0)
        machines, times = jobs[job_id][operation_index]

        # Find the best machine for the operation (earliest available time)
        best_machine, min_start_time, best_processing_time = None, float('inf'), None

        for m, t in zip(machines, times):
            start_time = max(machine_available_times[m], job_completion_times[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_processing_time = t

        # Schedule the operation on the best machine
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add the next operation of the job to the ready list, if it exists
        if operation_index + 1 < len(jobs[job_id]):
            ready_operations.append((job_id, operation_index + 1))

    return schedule
