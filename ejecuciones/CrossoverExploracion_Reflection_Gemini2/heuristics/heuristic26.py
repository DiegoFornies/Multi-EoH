
def heuristic(input_data):
    """Schedules jobs minimizing makespan using a greedy approach.

    It prioritizes operations based on shortest processing time first,
    then selects the earliest available machine that can execute the operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of all operations, sorted by shortest processing time.
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3]))  # Sort by shortest processing time

    for job, op_num, machines, times in operations:
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        # Find the best machine for the operation
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        end_time = best_start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
