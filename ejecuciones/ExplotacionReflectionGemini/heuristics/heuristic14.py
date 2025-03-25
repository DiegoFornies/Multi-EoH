
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with shorter processing times
    and assigns them to machines with the earliest available time.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_times = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of operations with job and op indices to sort by processing time
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx + 1, machines, times))

    # Sort the operations by minimum processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        # Find the best machine for the current operation
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Assign the operation to the best machine
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job] = max(job_completion_times[job], best_start_time + best_processing_time)

    return schedule
