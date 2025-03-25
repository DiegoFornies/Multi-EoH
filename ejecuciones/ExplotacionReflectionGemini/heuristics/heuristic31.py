
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes shortest processing time 
    and minimizes machine idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data}
    machine_available_times = {machine: 0 for machine in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}

    operations = []
    for job in jobs_data:
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time
    operations.sort(key=lambda op: min(op[3]))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine that minimizes the operation's start time
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        start_time = min_start_time
        end_time = start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
